"""
Monte Carlo Portfolio Retirement Simulator v3.0
================================================

NEW IN v3.0:
- 4 Portfolio Presets to Choose From:
  1. Dividend-Focused (Original - VTI/SCHG/SCHD/SGOV)
  2. Classic Three-Fund Bogleheads (VTI/VXUS/BND)
  3. Golden Butterfly / All-Weather (VTI/VXUS/SHY/TLT/GLD)
  4. Modern Bogleheads with TIPS (VTI/VXUS/VNQ/VTIP/BND)

All portfolios use:
- Geometric returns (volatility-adjusted)
- Annual rebalancing
- Realistic correlations
- Actual ETF expense ratios
- Investment fee modeling
- Optional fat-tail mode

IMPORTANT TAX NOTE:
This calculator does NOT include tax calculations as it's designed for global usage.
Tax treatment varies significantly by country, account type (taxable/retirement), and
individual circumstances. Please consult with a tax professional in your jurisdiction
to understand the after-tax impact of withdrawals.
"""

import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
import argparse

# --- 1. SIMULATION PARAMETERS ---
N_SIMULATIONS = 100_000      # Number of simulated paths
N_YEARS = 50                 # Simulation duration in years
INITIAL_VALUE = 1_000_000.0  # Starting portfolio value in dollars

# Withdrawal parameters (decimal: 0.03 = 3%)
# Uses constant dollar withdrawal strategy: withdraw X% of INITIAL portfolio value
# in year 1, then adjust for inflation each subsequent year.
# Note: Command-line argument accepts percentage (3.0) and converts to decimal
WITHDRAWAL_RATE = 0.03  # 3% of initial portfolio value (as decimal)

# Inflation (for real return comparison)
INFLATION_RATE = 0.025  # 2.5% annual inflation

# Investment fees (BEYOND individual ETF expense ratios)
ADDITIONAL_FEE = 0.00  # 0.00% = DIY investor (just ETF expenses)
                        # 0.0025 = 0.25% robo-advisor fee
                        # 0.01 = 1.00% traditional advisor fee

# Black swan modeling (optional)
BLACK_SWAN_MODE = False  # Set to True to model fat tails

# --- 2. PORTFOLIO DEFINITIONS ---

def arithmetic_to_geometric(arith_mean, std_dev):
    """Convert arithmetic mean to geometric mean."""
    return arith_mean - (std_dev ** 2) / 2

# Portfolio Preset 1: Dividend-Focused (Your Original)
PORTFOLIO_1 = {
    'name': 'Dividend-Focused Portfolio',
    'description': 'Heavy dividend tilt with growth and treasuries',
    'assets': {
        'VTI':  {'arith_mean': 0.10,  'sd': 0.17, 'weight': 0.35, 'er': 0.0003, 'name': 'Vanguard Total Stock Market'},
        'SCHG': {'arith_mean': 0.105, 'sd': 0.18, 'weight': 0.15, 'er': 0.0004, 'name': 'Schwab US Large-Cap Growth'},
        'SCHD': {'arith_mean': 0.115, 'sd': 0.17, 'weight': 0.30, 'er': 0.0006, 'name': 'Schwab US Dividend Equity'},
        'SGOV': {'arith_mean': 0.04,  'sd': 0.02, 'weight': 0.20, 'er': 0.0009, 'name': 'iShares 0-3 Month Treasury'}
    },
    'correlation': np.array([
        [1.00, 0.90, 0.80, 0.10],  # VTI
        [0.90, 1.00, 0.70, 0.10],  # SCHG
        [0.80, 0.70, 1.00, 0.15],  # SCHD
        [0.10, 0.10, 0.15, 1.00]   # SGOV
    ])
}

# Portfolio Preset 2: Classic Three-Fund Bogleheads
PORTFOLIO_2 = {
    'name': 'Classic Three-Fund Bogleheads',
    'description': 'The ultimate simple, diversified portfolio',
    'assets': {
        'VTI':  {'arith_mean': 0.10,  'sd': 0.17, 'weight': 0.54, 'er': 0.0003, 'name': 'Vanguard Total Stock Market'},
        'VXUS': {'arith_mean': 0.08,  'sd': 0.18, 'weight': 0.26, 'er': 0.0007, 'name': 'Vanguard Total International Stock'},
        'BND':  {'arith_mean': 0.04,  'sd': 0.03, 'weight': 0.20, 'er': 0.0003, 'name': 'Vanguard Total Bond Market'}
    },
    'correlation': np.array([
        [1.00, 0.85, 0.15],  # VTI
        [0.85, 1.00, 0.10],  # VXUS
        [0.15, 0.10, 1.00]   # BND
    ])
}

# Portfolio Preset 3: Golden Butterfly / All-Weather
PORTFOLIO_3 = {
    'name': 'Golden Butterfly (All-Weather)',
    'description': 'Designed for all market conditions with gold',
    'assets': {
        'VTI':  {'arith_mean': 0.10,  'sd': 0.17, 'weight': 0.30, 'er': 0.0003, 'name': 'Vanguard Total Stock Market'},
        'VXUS': {'arith_mean': 0.08,  'sd': 0.18, 'weight': 0.10, 'er': 0.0007, 'name': 'Vanguard Total International'},
        'SHY':  {'arith_mean': 0.025, 'sd': 0.01, 'weight': 0.20, 'er': 0.0015, 'name': 'iShares 1-3 Year Treasury'},
        'TLT':  {'arith_mean': 0.05,  'sd': 0.12, 'weight': 0.20, 'er': 0.0015, 'name': 'iShares 20+ Year Treasury'},
        'GLD':  {'arith_mean': 0.045, 'sd': 0.16, 'weight': 0.20, 'er': 0.0040, 'name': 'SPDR Gold Trust'}
    },
    'correlation': np.array([
        [1.00, 0.85, 0.10, -0.05, 0.00],  # VTI
        [0.85, 1.00, 0.10, -0.05, 0.00],  # VXUS
        [0.10, 0.10, 1.00,  0.40, 0.05],  # SHY
        [-0.05, -0.05, 0.40, 1.00, 0.10],  # TLT
        [0.00, 0.00, 0.05, 0.10, 1.00]    # GLD
    ])
}

# Portfolio Preset 4: Modern Bogleheads with TIPS and REITs
PORTFOLIO_4 = {
    'name': 'Modern Bogleheads (TIPS & REITs)',
    'description': 'Enhanced diversification with inflation protection',
    'assets': {
        'VTI':  {'arith_mean': 0.10,  'sd': 0.17, 'weight': 0.40, 'er': 0.0003, 'name': 'Vanguard Total Stock Market'},
        'VXUS': {'arith_mean': 0.08,  'sd': 0.18, 'weight': 0.20, 'er': 0.0007, 'name': 'Vanguard Total International'},
        'VNQ':  {'arith_mean': 0.09,  'sd': 0.20, 'weight': 0.10, 'er': 0.0012, 'name': 'Vanguard Real Estate ETF'},
        'VTIP': {'arith_mean': 0.03,  'sd': 0.03, 'weight': 0.15, 'er': 0.0004, 'name': 'Vanguard Short-Term TIPS'},
        'BND':  {'arith_mean': 0.04,  'sd': 0.03, 'weight': 0.15, 'er': 0.0003, 'name': 'Vanguard Total Bond Market'}
    },
    'correlation': np.array([
        [1.00, 0.85, 0.75, 0.10, 0.15],  # VTI
        [0.85, 1.00, 0.70, 0.10, 0.10],  # VXUS
        [0.75, 0.70, 1.00, 0.20, 0.20],  # VNQ
        [0.10, 0.10, 0.20, 1.00, 0.70],  # VTIP
        [0.15, 0.10, 0.20, 0.70, 1.00]   # BND
    ])
}

# All portfolios
PORTFOLIOS = {
    1: PORTFOLIO_1,
    2: PORTFOLIO_2,
    3: PORTFOLIO_3,
    4: PORTFOLIO_4
}

# --- 3. COMMAND LINE ARGUMENT PARSING ---
parser = argparse.ArgumentParser(description='Monte Carlo Retirement Simulator')
parser.add_argument('--portfolio', type=int, choices=[1, 2, 3, 4], default=1,
                    help='Portfolio preset (1=Dividend-Focused, 2=Three-Fund, 3=Golden Butterfly, 4=Modern Bogleheads)')
parser.add_argument('--withdrawal-rate', type=float, default=3.0,
                    help='Annual withdrawal rate as percentage (default: 3.0 = 3%%)')
parser.add_argument('--withdrawal-strategy', type=str, choices=['constant', 'dynamic'], default='constant',
                    help='Withdrawal strategy: constant (fixed inflation-adjusted) or dynamic (Vanguard Dynamic Spending)')
parser.add_argument('--dynamic-floor', type=float, default=2.5,
                    help='Dynamic spending floor percentage below inflation-adjusted spending (default: 2.5%%)')
parser.add_argument('--dynamic-ceiling', type=float, default=5.0,
                    help='Dynamic spending ceiling percentage above inflation-adjusted spending (default: 5.0%%)')
parser.add_argument('--years', type=int, default=50,
                    help='Simulation duration in years (default: 50)')
parser.add_argument('--initial', type=float, default=1_000_000,
                    help='Initial portfolio value (default: 1000000)')
parser.add_argument('--simulations', type=int, default=100_000,
                    help='Number of simulation paths (default: 100000)')
parser.add_argument('--fat-tails', action='store_true',
                    help='Enable fat-tail mode (Student t-distribution)')
parser.add_argument('--advisor-fee', type=float, default=0.00,
                    help='Additional advisor/platform fee %% (default: 0.00, example: 0.25 for 0.25%%)')
parser.add_argument('--list-portfolios', action='store_true',
                    help='List all available portfolios and exit')

args = parser.parse_args()

# List portfolios and exit if requested
if args.list_portfolios:
    print("\n" + "="*70)
    print("AVAILABLE PORTFOLIO PRESETS")
    print("="*70 + "\n")
    for num, portfolio in PORTFOLIOS.items():
        print(f"Portfolio {num}: {portfolio['name']}")
        print(f"Description: {portfolio['description']}")
        print(f"Assets:")
        total_er = 0
        for ticker, params in portfolio['assets'].items():
            print(f"  {ticker:5s}: {params['weight']:5.1%} | {params['name']}")
            total_er += params['er'] * params['weight']
        print(f"Blended Expense Ratio: {total_er:.4%}")
        print()
    exit(0)

# Update parameters from command line
N_SIMULATIONS = args.simulations
N_YEARS = args.years
INITIAL_VALUE = args.initial
WITHDRAWAL_RATE = args.withdrawal_rate / 100  # Convert from % to decimal
WITHDRAWAL_STRATEGY = args.withdrawal_strategy
DYNAMIC_FLOOR_PCT = args.dynamic_floor / 100  # Convert from % to decimal
DYNAMIC_CEILING_PCT = args.dynamic_ceiling / 100  # Convert from % to decimal
BLACK_SWAN_MODE = args.fat_tails
ADDITIONAL_FEE = args.advisor_fee / 100  # Convert from % to decimal

# Select portfolio
selected_portfolio = PORTFOLIOS[args.portfolio]
ASSETS_CONFIG = selected_portfolio['assets']
CORR_MATRIX = selected_portfolio['correlation']

# --- 4. PREPARE ASSETS FOR SIMULATION ---
asset_names = list(ASSETS_CONFIG.keys())
mean_returns = np.array([ASSETS_CONFIG[a]['arith_mean'] for a in asset_names])
std_devs = np.array([ASSETS_CONFIG[a]['sd'] for a in asset_names])
weights = np.array([ASSETS_CONFIG[a]['weight'] for a in asset_names])
expense_ratios = np.array([ASSETS_CONFIG[a]['er'] for a in asset_names])

# Convert to geometric returns
geometric_returns = np.array([arithmetic_to_geometric(ASSETS_CONFIG[a]['arith_mean'], ASSETS_CONFIG[a]['sd'])
                               for a in asset_names])

# Calculate blended expense ratio
blended_er = np.sum(expense_ratios * weights)
total_fee = blended_er + ADDITIONAL_FEE

# Adjust returns for fees
mean_returns_after_fees = geometric_returns - total_fee

# Build covariance matrix
cov_matrix = np.outer(std_devs, std_devs) * CORR_MATRIX

portfolio_exp_nominal_return = np.sum(mean_returns_after_fees * weights)
portfolio_exp_real_return = (1 + portfolio_exp_nominal_return) / (1 + INFLATION_RATE) - 1

# S&P 500 Proxy (for comparison)
SP500_PROXY = {
    'mean': arithmetic_to_geometric(0.10, 0.16),
    'sd': 0.16,
    'er': 0.0003  # VOO/SPY expense ratio
}
sp500_mean_after_fees = SP500_PROXY['mean'] - SP500_PROXY['er'] - ADDITIONAL_FEE

# --- 5. SIMULATION WITH REBALANCING ---
def run_simulation_with_rebalancing(n_sims, n_years, initial_value, withdrawal_rate,
                                     weights, multi_asset_returns, strategy='constant',
                                     floor_pct=0.025, ceiling_pct=0.05):
    """Monthly simulation with annual rebalancing to target weights.

    Supports two withdrawal strategies:

    CONSTANT DOLLAR (traditional SWR):
    - Year 1: Withdraw (initial_value * withdrawal_rate) / 12 each month
    - Year 2+: Withdraw same amount adjusted for inflation

    DYNAMIC SPENDING (Vanguard):
    - Calculate raw spending: current_portfolio * withdrawal_rate
    - Calculate floor: last_year_spending * (1 + inflation) * (1 - floor_pct)
    - Calculate ceiling: last_year_spending * (1 + inflation) * (1 + ceiling_pct)
    - Use raw if between floor/ceiling, otherwise use bound

    Process each month:
    1. Apply returns to FULL portfolio balance during month
    2. Withdraw at END of month (after returns)
    3. Rebalance annually (December)
    """
    n_assets = len(weights)
    n_months = n_years * 12

    # Initialize portfolio
    asset_values = np.zeros((n_sims, n_assets), dtype=np.float64)
    asset_values[:] = initial_value * weights

    # Storage for results (store monthly, but we'll aggregate to annual for output)
    monthly_withdrawals = np.zeros((n_months, n_sims), dtype=np.float64)
    monthly_values = np.zeros((n_months + 1, n_sims), dtype=np.float64)
    monthly_values[0] = initial_value

    # Calculate initial ANNUAL withdrawal amount
    initial_annual_withdrawal = initial_value * withdrawal_rate

    # Track last year's spending for each simulation (for dynamic strategy)
    last_year_spending = np.full(n_sims, initial_annual_withdrawal)

    for month in range(n_months):
        year_index = month // 12  # Which year are we in (for returns)
        month_in_year = month % 12  # Which month within the year

        # 1. APPLY RETURNS FIRST (during the month)
        # Convert annual returns to monthly (geometric)
        monthly_return = (1 + multi_asset_returns[year_index]) ** (1/12) - 1
        asset_values *= (1 + monthly_return)

        # Get portfolio value after returns
        portfolio_values = asset_values.sum(axis=1)

        # 2. CALCULATE ANNUAL WITHDRAWAL at start of each year (January)
        if month_in_year == 0:
            if strategy == 'constant':
                # CONSTANT DOLLAR: Fixed amount adjusted for inflation
                annual_withdrawal = initial_annual_withdrawal * ((1 + INFLATION_RATE) ** year_index)
                annual_withdrawal_amounts = np.full(n_sims, annual_withdrawal)

            elif strategy == 'dynamic':
                # DYNAMIC SPENDING (Vanguard)
                if year_index == 0:
                    # Year 1: Use initial withdrawal rate
                    annual_withdrawal_amounts = portfolio_values * withdrawal_rate
                else:
                    # Calculate raw spending
                    raw_spending = portfolio_values * withdrawal_rate

                    # Calculate inflation-adjusted last year spending
                    inflation_adjusted_last = last_year_spending * (1 + INFLATION_RATE)

                    # Calculate floor and ceiling
                    floor = inflation_adjusted_last * (1 - floor_pct)
                    ceiling = inflation_adjusted_last * (1 + ceiling_pct)

                    # Apply bounds
                    annual_withdrawal_amounts = np.where(
                        raw_spending < floor, floor,
                        np.where(raw_spending > ceiling, ceiling, raw_spending)
                    )

                # Update last year spending for next iteration
                last_year_spending = annual_withdrawal_amounts.copy()

        # 3. WITHDRAW at END of month (after returns)
        monthly_withdrawal_amount = annual_withdrawal_amounts / 12
        withdrawals = monthly_withdrawal_amount.copy()

        # Cannot withdraw more than what's available
        withdrawals = np.minimum(withdrawals, portfolio_values)
        monthly_withdrawals[month] = withdrawals

        # Withdraw proportionally from each asset
        for i in range(n_assets):
            asset_values[:, i] -= withdrawals * weights[i]

        # Set negative values to 0 (portfolio depleted)
        asset_values[asset_values < 0] = 0

        # Get portfolio value after withdrawal
        portfolio_values = asset_values.sum(axis=1)

        # 4. REBALANCE annually (at end of December, month 11, 23, 35, etc.)
        if month_in_year == 11:
            non_zero_mask = portfolio_values > 0
            asset_values[non_zero_mask] = (portfolio_values[non_zero_mask, np.newaxis] * weights)

        # Store portfolio value
        monthly_values[month + 1] = portfolio_values

    # Aggregate monthly data to annual for reporting
    annual_withdrawals = np.zeros((n_years, n_sims), dtype=np.float64)
    annual_values = np.zeros((n_years + 1, n_sims), dtype=np.float64)

    annual_values[0] = initial_value
    for year in range(n_years):
        # Sum withdrawals for this year (12 months)
        start_month = year * 12
        end_month = start_month + 12
        annual_withdrawals[year] = monthly_withdrawals[start_month:end_month].sum(axis=0)

        # End-of-year portfolio value
        annual_values[year + 1] = monthly_values[end_month]

    final_portfolio_values = portfolio_values

    return final_portfolio_values, annual_withdrawals, annual_values

# --- 6. GENERATE RANDOM RETURNS ---
print("Generating random returns for simulation...")

if BLACK_SWAN_MODE:
    print("Using fat-tail distribution (Student's t, df=5) for black swan events")
    t_samples = np.random.standard_t(df=5, size=(N_YEARS, N_SIMULATIONS, len(mean_returns_after_fees)))
    multi_asset_returns = t_samples * std_devs + mean_returns_after_fees

    # Cap returns at realistic bounds to prevent mathematical impossibilities
    # Can't lose more than 95% in a year, and cap gains at 500%
    multi_asset_returns = np.clip(multi_asset_returns, -0.95, 5.0)

    t_samples_sp500 = np.random.standard_t(df=5, size=(N_YEARS, N_SIMULATIONS))
    annual_sp500_returns = t_samples_sp500 * SP500_PROXY['sd'] + sp500_mean_after_fees
    annual_sp500_returns = np.clip(annual_sp500_returns, -0.95, 5.0)
else:
    print("Using normal distribution (standard Monte Carlo)")
    multi_asset_returns = np.random.multivariate_normal(
        mean_returns_after_fees, cov_matrix, size=(N_YEARS, N_SIMULATIONS)
    )
    # Cap returns at realistic bounds even for normal distribution
    multi_asset_returns = np.clip(multi_asset_returns, -0.95, 5.0)

    annual_sp500_returns = np.random.normal(
        sp500_mean_after_fees, SP500_PROXY['sd'], size=(N_YEARS, N_SIMULATIONS)
    )
    annual_sp500_returns = np.clip(annual_sp500_returns, -0.95, 5.0)

# Run simulations
print(f"Running {N_SIMULATIONS:,} Monte Carlo simulations...")
final_portfolio_values, withdrawals_history, portfolio_values_over_time = run_simulation_with_rebalancing(
    N_SIMULATIONS, N_YEARS, INITIAL_VALUE, WITHDRAWAL_RATE, weights, multi_asset_returns,
    strategy=WITHDRAWAL_STRATEGY, floor_pct=DYNAMIC_FLOOR_PCT, ceiling_pct=DYNAMIC_CEILING_PCT
)

sp500_weights = np.array([1.0])
sp500_returns_reshaped = annual_sp500_returns[:, :, np.newaxis]
final_sp500_values, _, sp500_values_over_time = run_simulation_with_rebalancing(
    N_SIMULATIONS, N_YEARS, INITIAL_VALUE, WITHDRAWAL_RATE, sp500_weights, sp500_returns_reshaped,
    strategy=WITHDRAWAL_STRATEGY, floor_pct=DYNAMIC_FLOOR_PCT, ceiling_pct=DYNAMIC_CEILING_PCT
)

# --- 7. CALCULATE METRICS ---
print("Calculating performance metrics...")

inflation_adjustor = (1 + INFLATION_RATE) ** N_YEARS
final_real_values = final_portfolio_values / inflation_adjustor
final_sp500_real = final_sp500_values / inflation_adjustor

avg_end_nominal = np.mean(final_portfolio_values)
med_end_nominal = np.median(final_portfolio_values)
p5_end_nominal = np.percentile(final_portfolio_values, 5)
p95_end_nominal = np.percentile(final_portfolio_values, 95)

avg_end_real = np.mean(final_real_values)
med_end_real = np.median(final_real_values)
p5_end_real = np.percentile(final_real_values, 5)
p95_end_real = np.percentile(final_real_values, 95)

# Use threshold for depletion check to handle floating point precision
# Consider portfolio depleted if value is less than $1
DEPLETION_THRESHOLD = 1.0
prob_depletion = np.sum(final_portfolio_values < DEPLETION_THRESHOLD) / N_SIMULATIONS
prob_beat_sp500_nominal = np.sum(final_portfolio_values > final_sp500_values) / N_SIMULATIONS
prob_beat_sp500_real = np.sum(final_real_values > final_sp500_real) / N_SIMULATIONS

def calculate_max_drawdown(values_over_time):
    running_max = np.maximum.accumulate(values_over_time, axis=0)
    drawdown = (running_max - values_over_time) / np.where(running_max == 0, 1, running_max)
    return np.max(drawdown, axis=0)

portfolio_max_drawdowns = calculate_max_drawdown(portfolio_values_over_time)
sp500_max_drawdowns = calculate_max_drawdown(sp500_values_over_time)

def find_failure_years(values_over_time):
    depleted = values_over_time < DEPLETION_THRESHOLD
    failure_years = np.argmax(depleted, axis=0)
    never_depleted = ~depleted.any(axis=0)
    failure_years[never_depleted] = N_YEARS + 1
    return failure_years

portfolio_failure_years = find_failure_years(portfolio_values_over_time)
depleted_mask = portfolio_failure_years <= N_YEARS

annual_returns = (final_portfolio_values / INITIAL_VALUE) ** (1/N_YEARS) - 1
risk_free_rate = 0.03

sharpe_ratio = (annual_returns.mean() - risk_free_rate) / annual_returns.std()

downside_returns = annual_returns - risk_free_rate
downside_returns[downside_returns > 0] = 0
downside_std = np.sqrt(np.mean(downside_returns ** 2))
sortino_ratio = (annual_returns.mean() - risk_free_rate) / downside_std if downside_std > 0 else np.inf

goals = [1_500_000, 2_000_000, 3_000_000, 5_000_000, 10_000_000]
goal_probabilities = {goal: np.mean(final_portfolio_values >= goal) for goal in goals}

# Fee impact calculation
gross_return = portfolio_exp_nominal_return + total_fee
fee_impact_total = (1 + gross_return) ** N_YEARS / (1 + portfolio_exp_nominal_return) ** N_YEARS - 1
fee_cost_on_initial = INITIAL_VALUE * fee_impact_total

# --- 8. DISPLAY RESULTS ---
print("\n" + "="*70)
print("MONTE CARLO PORTFOLIO RETIREMENT SIMULATOR v3.0")
print("="*70)
print(f"\n--- Selected Portfolio: {selected_portfolio['name']} ---")
print(f"Description: {selected_portfolio['description']}\n")

print("--- Simulation Setup ---")
print(f"Initial Portfolio Value: ${INITIAL_VALUE:,.0f}")

if WITHDRAWAL_STRATEGY == 'constant':
    print(f"Withdrawal Strategy: Constant Dollar (Traditional SWR)")
    print(f"  - Year 1: ${INITIAL_VALUE * WITHDRAWAL_RATE:,.0f} total ({WITHDRAWAL_RATE:.1%} of initial)")
    print(f"  - Year 2+: Inflation-adjusted (2.5% annual)")
    print(f"  - Monthly: Fixed amount divided by 12")
elif WITHDRAWAL_STRATEGY == 'dynamic':
    print(f"Withdrawal Strategy: Dynamic Spending (Vanguard Method)")
    print(f"  - Target Rate: {WITHDRAWAL_RATE:.1%} of portfolio balance")
    print(f"  - Floor: -{DYNAMIC_FLOOR_PCT:.1%} below inflation-adjusted prior year")
    print(f"  - Ceiling: +{DYNAMIC_CEILING_PCT:.1%} above inflation-adjusted prior year")
    print(f"  - Adjusts annually based on portfolio performance")

print(f"  - Timing: Returns applied first, withdrawals at END of month")
print(f"Simulation: {N_SIMULATIONS:,} paths over {N_YEARS} years ({N_YEARS * 12:,} months)")
print(f"Rebalancing: Annual rebalancing to target weights")
print(f"Return Type: Geometric means (volatility-adjusted)")
print(f"Distribution: {'Student t (df=5) - Fat tails' if BLACK_SWAN_MODE else 'Normal - Standard Monte Carlo'}")
print()

print("--- Portfolio Allocation ---")
for ticker, params in ASSETS_CONFIG.items():
    geom_before_fees = arithmetic_to_geometric(params['arith_mean'], params['sd'])
    geom_after_fees = geom_before_fees - params['er'] - ADDITIONAL_FEE
    print(f"{ticker:5s}: {params['weight']:5.1%} | ER: {params['er']:.4%} | "
          f"Arith: {params['arith_mean']:5.1%} | Geom: {geom_before_fees:5.1%} | "
          f"After Fees: {geom_after_fees:5.1%} | Vol: {params['sd']:5.1%}")

print("\n--- Fee Breakdown ---")
print(f"Portfolio Blended Expense Ratio: {blended_er:.4%}")
if ADDITIONAL_FEE > 0:
    print(f"Additional Advisor/Platform Fee: {ADDITIONAL_FEE:.4%}")
print(f"Total Annual Fee: {total_fee:.4%}")
print(f"Gross Return (before all fees): {gross_return:.2%}")
print(f"Net Return (after all fees): {portfolio_exp_nominal_return:.2%}")
print(f"Fee drag over {N_YEARS} years: {fee_impact_total:.1%}")
print(f"Cost of fees on ${INITIAL_VALUE:,.0f}: ${fee_cost_on_initial:,.0f}")

print("\n" + "-"*70)
print("\n--- PORTFOLIO PERFORMANCE SUMMARY ---")

results_data = {
    "Metric": [
        "Average Ending Value",
        "Median Ending Value",
        "5th Percentile",
        "95th Percentile",
        "Probability of Depletion",
        "Median Max Drawdown",
        "95th %ile Max Drawdown"
    ],
    "Nominal Value": [
        f"${avg_end_nominal:,.0f}",
        f"${med_end_nominal:,.0f}",
        f"${p5_end_nominal:,.0f}",
        f"${p95_end_nominal:,.0f}",
        f"{prob_depletion:.2%}",
        f"{np.median(portfolio_max_drawdowns):.1%}",
        f"{np.percentile(portfolio_max_drawdowns, 95):.1%}"
    ],
    "Real Value (Today's $)": [
        f"${avg_end_real:,.0f}",
        f"${med_end_real:,.0f}",
        f"${p5_end_real:,.0f}",
        f"${p95_end_real:,.0f}",
        "N/A",
        "N/A",
        "N/A"
    ]
}
results_df = pd.DataFrame(results_data)
print(results_df.to_string(index=False))

print("\n" + "-"*70)
print("\n--- WITHDRAWAL ANALYSIS ---")

withdrawals_mean = withdrawals_history.mean(axis=1)
withdrawals_median = np.median(withdrawals_history, axis=1)
withdrawals_p5 = np.percentile(withdrawals_history, 5, axis=1)
withdrawals_p95 = np.percentile(withdrawals_history, 95, axis=1)

withdrawals_df = pd.DataFrame({
    "Year": np.arange(1, N_YEARS + 1),
    "Average": withdrawals_mean,
    "Median": withdrawals_median,
    "5th %ile": withdrawals_p5,
    "95th %ile": withdrawals_p95
})

print("First 10 Years:")
print(withdrawals_df.head(10).to_string(index=False, float_format=lambda x: f'${x:,.0f}'))
print("\nLast 10 Years:")
print(withdrawals_df.tail(10).to_string(index=False, float_format=lambda x: f'${x:,.0f}'))

print("\n" + "-"*70)
print("\n--- RISK METRICS ---")
print(f"Portfolio Sharpe Ratio: {sharpe_ratio:.2f}")
print(f"Portfolio Sortino Ratio: {sortino_ratio:.2f}")
print(f"Median Maximum Drawdown: {np.median(portfolio_max_drawdowns):.1%}")
print(f"Worst Drawdown (95th %ile): {np.percentile(portfolio_max_drawdowns, 95):.1%}")

if depleted_mask.any():
    print(f"\nPortfolios Depleted: {depleted_mask.sum():,} ({depleted_mask.mean():.2%})")
    print(f"Median Failure Year: {np.median(portfolio_failure_years[depleted_mask]):.0f}")
else:
    print(f"\nPortfolios Depleted: None (0.00%)")

print("\n" + "-"*70)
print("\n--- GOAL PROBABILITY ANALYSIS ---")
print("Probability of reaching target by end of simulation:")
for goal in goals:
    prob = goal_probabilities[goal]
    print(f"  ${goal:>10,}: {prob:>6.1%}")

print("\n" + "-"*70)
print("\n--- BENCHMARK COMPARISON (S&P 500) ---")
print(f"S&P 500 Median Ending (Nominal): ${np.median(final_sp500_values):,.0f}")
print(f"S&P 500 Median Ending (Real):    ${np.median(final_sp500_real):,.0f}")
print(f"Portfolio Beats S&P 500 (Nominal): {prob_beat_sp500_nominal:.1%}")
print(f"Portfolio Beats S&P 500 (Real):    {prob_beat_sp500_real:.1%}")
print(f"S&P 500 Median Max Drawdown: {np.median(sp500_max_drawdowns):.1%}")

print("\n" + "-"*70)
print("\n--- EXPECTED RETURNS ---")
print(f"Portfolio Exp. Nominal (before fees): {gross_return:.2%}")
print(f"Portfolio Exp. Nominal (after fees):  {portfolio_exp_nominal_return:.2%}")
print(f"Portfolio Exp. Real (after fees):     {portfolio_exp_real_return:.2%}")

# --- 9. EXPORT TO CSV ---
output_dir = Path(__file__).parent / "outputs"
output_dir.mkdir(exist_ok=True)

portfolio_name_safe = selected_portfolio['name'].replace(' ', '_').replace('/', '_')
results_df.to_csv(output_dir / f'results_{portfolio_name_safe}_v3.csv', index=False)
withdrawals_df.to_csv(output_dir / f'withdrawals_{portfolio_name_safe}_v3.csv', index=False)

percentile_paths = pd.DataFrame({
    'Year': np.arange(N_YEARS + 1),
    'P5_Nominal': np.percentile(portfolio_values_over_time, 5, axis=1),
    'P25_Nominal': np.percentile(portfolio_values_over_time, 25, axis=1),
    'P50_Nominal': np.percentile(portfolio_values_over_time, 50, axis=1),
    'P75_Nominal': np.percentile(portfolio_values_over_time, 75, axis=1),
    'P95_Nominal': np.percentile(portfolio_values_over_time, 95, axis=1),
    'P5_Real': np.percentile(portfolio_values_over_time, 5, axis=1) / ((1 + INFLATION_RATE) ** np.arange(N_YEARS + 1)),
    'P50_Real': np.percentile(portfolio_values_over_time, 50, axis=1) / ((1 + INFLATION_RATE) ** np.arange(N_YEARS + 1)),
    'P95_Real': np.percentile(portfolio_values_over_time, 95, axis=1) / ((1 + INFLATION_RATE) ** np.arange(N_YEARS + 1)),
})
percentile_paths.to_csv(output_dir / f'paths_{portfolio_name_safe}_v3.csv', index=False)

print("\n" + "="*70)
print("EXPORT COMPLETE")
print("="*70)
print(f"\nResults exported to: {output_dir}/")
print(f"  - results_{portfolio_name_safe}_v3.csv")
print(f"  - withdrawals_{portfolio_name_safe}_v3.csv")
print(f"  - paths_{portfolio_name_safe}_v3.csv")

print("\n" + "="*70)
print("USAGE EXAMPLES")
print("="*70)
print("""
# List all available portfolios
python SWR_Monte_Carlo.py --list-portfolios

# Run Classic Three-Fund Bogleheads (constant dollar withdrawal)
python SWR_Monte_Carlo.py --portfolio 2

# Run with Vanguard Dynamic Spending strategy
python SWR_Monte_Carlo.py --portfolio 2 --withdrawal-strategy dynamic

# Customize dynamic spending bounds (3% floor, 6% ceiling)
python SWR_Monte_Carlo.py --portfolio 2 --withdrawal-strategy dynamic \\
  --dynamic-floor 3.0 --dynamic-ceiling 6.0

# Run Golden Butterfly with 4% withdrawal rate
python SWR_Monte_Carlo.py --portfolio 3 --withdrawal-rate 4.0

# Run with fat-tail mode and 0.25% advisor fee
python SWR_Monte_Carlo.py --portfolio 4 --fat-tails --advisor-fee 0.25

# 30-year simulation with $2M starting value
python SWR_Monte_Carlo.py --portfolio 2 --years 30 --initial 2000000

# Compare constant vs dynamic strategies
python SWR_Monte_Carlo.py --portfolio 2 --withdrawal-rate 4.0
python SWR_Monte_Carlo.py --portfolio 2 --withdrawal-rate 4.0 --withdrawal-strategy dynamic
""")

print("\n" + "="*70)
print("Simulation complete!")
print("="*70)
