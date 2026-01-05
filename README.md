# SWR Monte Carlo Retirement Simulation

I decided it was time to take a different approach since I already created a Safe Withdrawal Rate Calculator based on historical data (1871 to 2024). This online calculator is available on my webpage https://finfr.ee. 
Feel free to check it out. That's how my new Safe Withdrawal Rate Calculator using Monte Carlo Simulation was born. 
So here it is, my very own professional Monte Carlo simulation tool for retirement planning with Safe Withdrawal Rate (SWR) analysis using 4 known portfolio strategies based on Bogleheads principles.

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)

---

## 🎯 What This Does

Run thousands of **monthly-precision** retirement simulations to answer:
- **Will my money last?** (Depletion probability)
- **What's my worst-case outcome?** (5th percentile)
- **How much volatility should I expect?** (Maximum drawdown)
- **Is 2.5-3% withdrawal rate safe? What about 4%?**

**Unlike simple calculators**, this one models:
- ✅ **Monthly simulation** (600 months for 50 years) for accurate modeling
- ✅ **Two withdrawal strategies**: Constant dollar (traditional SWR) & Dynamic spending (Vanguard method)
- ✅ Market volatility (not just average returns)
- ✅ Sequence of returns risk
- ✅ Annual rebalancing
- ✅ Investment fees and expense ratios
- ✅ Annual inflation adjustment (no monthly compounding)
- ✅ Correlation between assets (realistic co-movement)
- ✅ Optional black swan events (fat-tail mode)
- ✅ Geometric returns (volatility-adjusted, not arithmetic)

---

## 📊 4 Portfolio Strategies

### 1. Dividend-Focused Portfolio (my own!)
**Assets:** VTI (35%) • SCHG (15%) • SCHD (30%) • SGOV (20%)
**ER:** 0.0525% | **Best For:** Income seekers, dividend growth investors

### 2. Classic Three-Fund Bogleheads ⭐ **RECOMMENDED**
**Assets:** VTI (54%) • VXUS (26%) • BND (20%)
**ER:** 0.0404% | **Best For:** Most investors, simple & effective

### 3. Golden Butterfly / All-Weather
**Assets:** VTI (20%) • VXUS (20%) • SHY (20%) • TLT (20%) • GLD (20%)
**ER:** 0.1560% | **Best For:** Conservative investors, inflation protection

### 4. Modern Bogleheads with TIPS
**Assets:** VTI (42%) • VXUS (18%) • VNQ (5%) • VTIP (15%) • BND (20%)
**ER:** 0.0485% | **Best For:** Inflation-worried, diversification seekers

---

## 🚀 Quick Start

### Option 1: Docker (Recommended - No Setup Required) 
(Install Docker Desktop)

```bash
# 1. Clone repository
git clone https://github.com/leviceroy/SWR_Monte_Carlo.git
cd SWR_Monte_Carlo

# 2. Run with Docker Compose (auto-builds on first run)
docker-compose run --rm swr-monte-carlo

# That's it! Results saved to outputs/
```

**Customize parameters:**
```bash
docker-compose run --rm swr-monte-carlo python SWR_Monte_Carlo.py \
  --portfolio 2 \
  --initial-value 1000000 \
  --withdrawal-rate 3.5 \
  --years 50 \
  --simulations 50000 \
  --fat-tails
```

### Option 2: Local Python Installation

```bash
# 1. Clone repository
git clone https://github.com/leviceroy/SWR_Monte_Carlo.git
cd SWR_Monte_Carlo

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run simulation
python SWR_Monte_Carlo.py --portfolio 2 --withdrawal-rate 3.0
```

---

## 📖 Usage Examples

### Basic Simulation (Three-Fund Bogleheads, 3% withdrawal)
```bash
python SWR_Monte_Carlo.py --portfolio 2
```

### Dynamic Withdrawal Strategy (Vanguard Method)
```bash
python SWR_Monte_Carlo.py \
  --portfolio 2 \
  --withdrawal-rate 3.0 \
  --withdrawal-strategy dynamic
```

### Custom Dynamic Spending Bounds
```bash
python SWR_Monte_Carlo.py \
  --portfolio 2 \
  --withdrawal-strategy dynamic \
  --dynamic-floor 3.0 \
  --dynamic-ceiling 6.0
```

### Aggressive 4% Withdrawal with Fat-Tail Mode
```bash
python SWR_Monte_Carlo.py \
  --portfolio 2 \
  --withdrawal-rate 4.0 \
  --fat-tails
```

### Conservative Golden Butterfly, 2.5% Withdrawal, 30 Years
```bash
python SWR_Monte_Carlo.py \
  --portfolio 3 \
  --withdrawal-rate 2.5 \
  --years 30
```

### Include 1% Advisor Fee (hope you don't choose an advisor wasting your money!)
```bash
python SWR_Monte_Carlo.py \
  --portfolio 2 \
  --advisor-fee 1.0
```

### High-Accuracy Simulation (100,000 paths)
```bash
python SWR_Monte_Carlo.py \
  --portfolio 2 \
  --simulations 100000
```

---

## 📋 Command-Line Options

| Parameter | Short | Default | Description |
|-----------|-------|---------|-------------|
| `--portfolio` | `-p` | `1` | Portfolio (1-4) |
| `--initial-value` | `-i` | `1000000` | Starting portfolio value |
| `--withdrawal-rate` | `-w` | `3.0` | Annual withdrawal % |
| `--withdrawal-strategy` | | `constant` | Withdrawal strategy: `constant` or `dynamic` |
| `--dynamic-floor` | | `2.5` | Dynamic spending floor % below inflation-adjusted |
| `--dynamic-ceiling` | | `5.0` | Dynamic spending ceiling % above inflation-adjusted |
| `--years` | `-y` | `50` | Retirement duration (years) |
| `--simulations` | `-s` | `100000` | Number of Monte Carlo paths |
| `--advisor-fee` | `-f` | `0.0` | Additional advisor fee % |
| `--fat-tails` | | `False` | Enable black swan modeling |
| `--list-portfolios` | | | List all available portfolios and exit |

**View all options:**
```bash
python SWR_Monte_Carlo.py --help
```

---

## 📊 Output Explained

### Terminal Output

```
╔══════════════════════════════════════════════════════════════╗
║          Monte Carlo Retirement Simulation Results           ║
╚══════════════════════════════════════════════════════════════╝

Portfolio: Classic Three-Fund Bogleheads
Parameters: $1,000,000 | 3.0% withdrawals | 50 years | 10,000 sims

PERCENTILE ANALYSIS (Nominal Values)
────────────────────────────────────
  5th Percentile:    $2,847,381  ← Worst case (95% confidence)
  Median (50th):    $12,847,293  ← Most likely
 95th Percentile:   $51,234,872  ← Best case (5% chance)

INFLATION-ADJUSTED (Real 2024 Dollars)
───────────────────────────────────────
  5th Percentile:      $645,123
  Median (50th):     $2,911,847
 95th Percentile:   $11,612,394

RISK METRICS
────────────
 Depletion Risk:        0.0%  ← Probability of running out
 Max Drawdown:        -42.3%  ← Worst peak-to-trough
 Sharpe Ratio:          1.24  ← Risk-adjusted returns

vs S&P 500 (with same withdrawals)
  Portfolio Median:  $12,847,293
  S&P 500 Median:    $14,234,123
  Difference:         -9.7%
```

### CSV Export

Results are automatically saved to `outputs/monte_carlo_results_YYYYMMDD_HHMMSS.csv`

---

## 🐳 Docker Setup

See [DOCKER_SETUP.md](DOCKER_SETUP.md) for detailed Docker instructions including:
- Installation on Windows/Mac/Linux
- Building custom images
- Volume mounting for outputs
- Troubleshooting

**Quick Docker commands:**

```bash
# Build image
docker-compose build

# Run simulation
docker-compose run --rm swr-monte-carlo

# Enter container (interactive)
docker-compose run --rm swr-monte-carlo /bin/bash

# Clean up
docker-compose down
docker rmi swr-monte-carlo
```

---

## 🔬 How It Works

### Monte Carlo Methodology (Monthly Simulation)

**For each of 10,000+ simulations:**

1. **Generate Random Annual Returns**: Sample from historical mean & standard deviation
2. **Apply Correlations**: Use Cholesky decomposition for realistic asset correlations
3. **Geometric Returns**: Adjust for volatility drag (arithmetic - σ²/2)
4. **Monthly Loop** (600 months for 50 years):
   - Convert annual returns to monthly: `(1 + annual_return)^(1/12) - 1`
   - Apply returns to full portfolio balance
   - Withdraw constant dollar amount at month end (1/12 of annual withdrawal)
   - Inflation adjustment applied ANNUALLY (not monthly compounding)
5. **Annual Rebalancing**: Reset to target allocation each December
6. **Track Statistics**: Record percentiles, drawdowns, depletion events

### Withdrawal Strategies

#### 1. Constant Dollar (Traditional SWR) - Default

**Year 1:** Withdraw X% of initial $1,000,000 = $30,000 (if 3%)
**Year 2:** Withdraw $30,000 × 1.025 (inflation) = $30,750
**Year 3:** Withdraw $30,750 × 1.025 = $31,519
**And so on...**

This matches the Trinity Study and traditional SWR research. Prioritizes inflation-adjusted stability to ensure a consistent quality of life regardless of market shifts.

#### 2. Dynamic Spending (Vanguard Method)

Adjusts withdrawals based on portfolio performance while maintaining guardrails:
- **Target:** X% of current portfolio balance
- **Floor:** Cannot drop more than 2.5% (default) below inflation-adjusted prior year
- **Ceiling:** Cannot rise more than 5.0% (default) above inflation-adjusted prior year
- **Benefit:** Reduces depletion risk significantly while allowing spending to grow with portfolio

This is different from "variable percentage withdrawal" where you simply withdraw X% of current balance with no guardrails. 

### Key Features

✅ **Monthly Precision** - 600 data points over 50 years (not just 50 annual)
✅ **Dual Withdrawal Strategies** - Traditional constant dollar + dynamic spending (Vanguard method)
✅ **Geometric Returns** - Not arithmetic (critical for accuracy)
✅ **Correct Order** - Returns applied first, then withdrawals
✅ **Annual Inflation** - 2.5% compounded yearly, not monthly
✅ **Rebalancing Bonus** - Annual rebalancing adds 0.3-0.5%/year
✅ **Realistic Correlations** - Assets don't move independently
✅ **Fee Modeling** - Includes ETF expense ratios + optional advisor fees
✅ **Fat-Tail Mode** - Student's t-distribution for black swan events
✅ **Depletion Threshold** - Uses <$1 threshold for accurate failure detection
✅ **Return Bounds** - Clips returns to realistic range (-95% to +500%)

### What This Model Cannot Do

⚠️ **Market Regime Changes** - Returns vary by decade (1970s: 5.9%, 2000s: -0.9%, 2010s: 13.6%)
⚠️ **True Black Swans** - Even fat-tail mode can't predict 2008-level crashes
⚠️ **Taxes** - Global tool, tax rules vary by country/account type. I did this on purpose.
⚠️ **Advanced Withdrawal Strategies** - No Guyton-Klinger or other complex rule-based strategies (yet)

---

## 🧪 Example Results

### Classic Three-Fund at Different Withdrawal Rates (50-Year Horizon)

| Withdrawal Rate | Depletion Risk | 5th Percentile | Median | Interpretation |
|-----------------|----------------|----------------|---------|----------------|
| **2.5%** | 12-13% | $0 | $7.7M | Very safe for most scenarios |
| **3.0%** | 23-25% | $0 | $5.2M | Safe with moderate risk |
| **3.5%** | 34-36% | $0 | $2.9M | Moderate risk, needs flexibility |
| **4.0%** | 47-50% | $0 | $390K | High risk for 50 years |
| **4.5%** | 60-65% | $0 | $0 | Very risky, not recommended |

**Important Notes:**
- These are for **50-year** retirements (age 50 → age 100)
- Uses **constant dollar withdrawals** (traditional SWR methodology)
- For **30-year** retirements: depletion rates are much lower (~2-5% at 3%, ~15-20% at 4%)
- "Depletion Risk" = probability portfolio reaches $0 before year 50
- 5th percentile of $0 doesn't mean total failure - just worst 5% scenarios deplete

**Interpretation:**
- **2.5-3% is very safe** for 50-year retirements
- **3.5-4% has moderate-high risk** for 50 years (but acceptable for 30 years)
- **4%+ is aggressive** for early retirees with 50-year horizons

### Dynamic vs Constant Withdrawal Strategy Comparison

**Dynamic Spending (Vanguard Method) Benefits:**
- **Lower depletion risk** - Typically 50-70% reduction in failure probability
- **Higher median outcomes** - Portfolio grows more in good markets
- **Flexibility** - Spending adjusts to market conditions
- **Upside potential** - Can spend more when portfolio performs well

**Trade-offs:**
- **Variable spending** - Annual withdrawals fluctuate (within guardrails)
- **Complexity** - Requires annual adjustments vs. set-it-and-forget-it
- **Psychological** - Must adapt lifestyle to changing withdrawal amounts

**When to use each:**
- **Constant:** Prefer predictable income, willing to accept higher depletion risk for stability
- **Dynamic:** Prefer flexibility, want to maximize portfolio longevity and upside potential

---

## 📚 Documentation

- **[ReadME_V3.md](ReadME_V3.md)** - Detailed technical documentation
- **[DOCKER_SETUP.md](DOCKER_SETUP.md)** - Complete Docker guide
- **[GITHUB_SETUP.md](GITHUB_SETUP.md)** - GitHub repository setup instructions

---

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- [ ] Additional withdrawal strategies (Guyton-Klinger, VPW)
- [ ] Tax modeling for different jurisdictions
- [ ] Web interface/GUI
- [ ] Historical backtesting mode

**If you want to contribute:**
1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open Pull Request

---

## 📝 License

MIT License - Free to use, modify, and distribute.

See [LICENSE](LICENSE) for details.

---

## ⚠️ Disclaimer

**This tool is for educational purposes only. NOT financial advice.**

- Past performance doesn't guarantee future results
- Consult qualified help before making investment decisions.
- Consider your personal circumstances, risk tolerance, and goals
- Tax implications vary by jurisdiction. 

**Financial calculations are estimates based on historical data and assumptions.**

---

## 🙏 Credits

**Based on:**
- Bogleheads investment philosophy
- Trinity Study (safe withdrawal rates)
- Modern Portfolio Theory
- Monte Carlo simulation techniques

**Built with:**
- Python 3.11
- NumPy (numerical computing)
- Pandas (data analysis)
- SciPy (statistical distributions)

---

## 📞 Support

**You got any Issues?**
- Check [DOCKER_SETUP.md](DOCKER_SETUP.md) for Docker troubleshooting
- Review [ReadME_V3.md](ReadME_V3.md) for technical details
- Open an issue on GitHub

**Questions?**
- Review documentation first
- Check existing GitHub issues
- Open new issue with details

---

## 📈 Roadmap

**Future Versions**
- [ ] Additional withdrawal strategies (Guyton-Klinger, VPW, CAPE-based)
- [ ] Tax modeling for different jurisdictions
- [ ] Web interface/GUI
- [ ] Historical backtesting mode
- [ ] Multi-currency support
- [ ] Social Security integration

---

## 📝 Changelog

### v3.2 (January 2026) - NEW FEATURE: Dynamic Withdrawal Strategy ✅

**🎯 Major New Feature:**

1. **Dynamic Withdrawal Strategy (Vanguard Method)** ✅ NEW
   - Adjusts withdrawals based on portfolio performance
   - Customizable floor and ceiling guardrails
   - Significantly reduces depletion risk vs constant withdrawals
   - Allows spending to grow with portfolio success

**Command-Line Additions:**
   - `--withdrawal-strategy {constant,dynamic}` - Choose withdrawal method
   - `--dynamic-floor X.X` - Set floor percentage (default: 2.5%)
   - `--dynamic-ceiling X.X` - Set ceiling percentage (default: 5.0%)
   - `--list-portfolios` - List all portfolio options

**Improvements:**
   - Updated Portfolio 1 allocations for better balance
   - Enhanced output formatting with withdrawal analysis tables
   - Better documentation of withdrawal strategies

### v3.1 (December 2025) - CRITICAL FIXES ✅

**🔧 BREAKING CHANGES - Results will differ significantly from v3.0**

This update corrects fundamental calculation errors to match industry-standard Safe Withdrawal Rate methodology:

**What Changed:**

1. **Withdrawal Strategy** ✅ FIXED
   - **OLD (WRONG):** Variable percentage withdrawal (withdraw X% of current balance each year)
   - **NEW (CORRECT):** Constant dollar withdrawal (withdraw X% of initial balance, inflation-adjusted annually)
   - **Impact:** Old method could never deplete portfolio mathematically. New method matches Trinity Study.

2. **Simulation Frequency** ✅ IMPROVED
   - **OLD:** Annual simulation (50 data points)
   - **NEW:** Monthly simulation (600 data points over 50 years)
   - **Impact:** More accurate modeling of real-world withdrawals and returns

3. **Order of Operations** ✅ FIXED
   - **OLD:** Withdraw first, then apply returns (wrong order)
   - **NEW:** Apply returns first, then withdraw at month end
   - **Impact:** Slightly more conservative (matches real portfolio behavior)

4. **Inflation Adjustment** ✅ FIXED
   - **OLD:** Monthly compounding inflation within each year
   - **NEW:** Annual inflation adjustment (2.5% applied once per year)
   - **Impact:** Old method withdrew ~1.14% more than intended per year

5. **Depletion Detection** ✅ FIXED
   - **OLD:** Exact $0 check (missed floating-point near-zero values)
   - **NEW:** Threshold-based (<$1 = depleted)
   - **Impact:** More accurate depletion probability reporting

6. **Return Bounds** ✅ ADDED
   - Clips returns to realistic range (-95% to +500%)
   - Prevents mathematical impossibilities with extreme returns

**Expected Result Changes:**
- **Depletion rates will be HIGHER** (but more accurate!)
- With 4% withdrawal over 50 years: ~40-50% depletion (was incorrectly 0%)
- With 3% withdrawal over 50 years: ~20-25% depletion (was incorrectly 0%)
- With 2.5% withdrawal over 50 years: ~12-15% depletion (was incorrectly 0%)

**Why This Matters:**
The v3.0 calculator gave false confidence because it used variable percentage withdrawals (which can never fully deplete) instead of constant dollar withdrawals (the standard SWR approach used in retirement research).

**If you made retirement decisions based on v3.0, please re-run your simulations with v3.1.**

**Verification:**
This version produces results consistent with:
- Trinity Study (1998)
- Early Retirement Now SWR Series
- cFIREsim and FIRECalc (historical calculators)

### v3.0 (Initial Release)
- 4 portfolio strategies
- Docker support
- Basic Monte Carlo simulation
- Fat-tail mode

---

**Ready to test your retirement plan?** 🎯

**Star ⭐ this repo if you find it useful!**
