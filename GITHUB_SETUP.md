# GitHub Repository Setup Guide

Step-by-step instructions for creating and managing the SWR_Monte_Carlo repository on GitHub.

---

## 🎯 Prerequisites

- GitHub account (create at https://github.com/signup if needed)
- Git installed locally
- Repository files ready (you have them!)

---

## 📝 Step 1: Create GitHub Repository

### Option A: Using GitHub Website (Easiest)

**1. Log in to GitHub:**
- Visit https://github.com
- Log in as `leviceroy`

**2. Create New Repository:**
- Click the **"+"** icon (top-right) → **"New repository"**
- Or visit: https://github.com/new

**3. Configure Repository:**
```
Repository name: SWR_Monte_Carlo
Description: Monte Carlo retirement simulator with 4 portfolio strategies. Safe Withdrawal Rate (SWR) analysis with realistic modeling.
Public/Private: ✅ Public (so others can use it)
Initialize: ❌ Do NOT check "Add a README" (we have one)
           ❌ Do NOT add .gitignore (we have one)
           ❌ Do NOT choose a license yet
```

**4. Click "Create repository"**

**5. Copy the repository URL:**
```
https://github.com/leviceroy/SWR_Monte_Carlo.git
```

---

### Option B: Using GitHub CLI (Alternative)

**Install GitHub CLI:**
```bash
# Linux (Ubuntu/Debian)
curl -fsSL https://cli.github.com/packages/githubcli-archive-keyring.gpg | sudo dd of=/usr/share/keyrings/githubcli-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/githubcli-archive-keyring.gpg] https://cli.github.com/packages stable main" | sudo tee /etc/apt/sources.list.d/github-cli.list > /dev/null
sudo apt update
sudo apt install gh

# macOS
brew install gh

# Windows
winget install --id GitHub.cli
```

**Create repository:**
```bash
# Login first
gh auth login

# Create repo
gh repo create leviceroy/SWR_Monte_Carlo --public --description "Monte Carlo retirement simulator with 4 portfolio strategies"
```

---

## 🏗️ Step 2: Initialize Local Git Repository

**Navigate to project directory:**
```bash
cd "/home/shinybunny/Pythonscripts/Monte/MonteCarlo Sim"
```

**Initialize Git:**
```bash
# Initialize repository
git init

# Verify .gitignore exists
cat .gitignore

# Add all files
git add .

# Check what will be committed
git status

# Create first commit
git commit -m "Initial commit: Monte Carlo retirement simulator v3.2

Features:
- 4 portfolio presets (Dividend, Three-Fund, Golden Butterfly, Modern Bogleheads)
- Geometric returns with annual rebalancing
- Fat-tail mode for black swan events
- Investment fee modeling
- Docker support
- Comprehensive documentation"
```

**Expected output:**
```
[main (root-commit) abc1234] Initial commit: Monte Carlo retirement simulator v3.2
 10 files changed, 2847 insertions(+)
 create mode 100644 .dockerignore
 create mode 100644 .gitignore
 create mode 100644 DOCKER_SETUP.md
 create mode 100644 Dockerfile
 create mode 100644 GITHUB_SETUP.md
 create mode 100644 README.md
 create mode 100644 ReadME_V3.md
 create mode 100644 SWR_Monte_Carlo.py
 create mode 100644 docker-compose.yml
 create mode 100644 requirements.txt
 create mode 100644 outputs/.gitkeep
```

---

## 🔗 Step 3: Connect to GitHub

**Add remote:**
```bash
git remote add origin https://github.com/leviceroy/SWR_Monte_Carlo.git

# Verify
git remote -v
```

**Expected output:**
```
origin  https://github.com/leviceroy/SWR_Monte_Carlo.git (fetch)
origin  https://github.com/leviceroy/SWR_Monte_Carlo.git (push)
```

---

## 📤 Step 4: Push to GitHub

**Push to remote:**
```bash
# Rename branch to 'main' (GitHub default)
git branch -M main

# Push to GitHub
git push -u origin main
```

**First time?** You'll be prompted for credentials:
```
Username for 'https://github.com': leviceroy
Password for 'https://leviceroy@github.com': [use Personal Access Token, not password]
```

---

## 🔑 Setting Up Authentication

### Option 1: Personal Access Token (Recommended)

**Why?** GitHub no longer accepts passwords for Git operations.

**Steps:**
1. Go to GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
2. Or visit: https://github.com/settings/tokens
3. Click **"Generate new token"** → **"Generate new token (classic)"**
4. Configure:
   ```
   Note: SWR Monte Carlo - Git access
   Expiration: 90 days (or your preference)
   Scopes:
     ✅ repo (all)
     ✅ workflow (if using GitHub Actions)
   ```
5. Click **"Generate token"**
6. **COPY THE TOKEN NOW** (you can't see it again!)
7. Use token as password when pushing

**Save token securely:**
```bash
# Configure Git to remember credentials (Linux/Mac)
git config --global credential.helper store

# Now push (will ask for credentials once)
git push -u origin main

# Enter:
# Username: leviceroy
# Password: ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx (your token)

# Future pushes won't ask for credentials
```

---

### Option 2: SSH Keys (Alternative)

**Generate SSH key:**
```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
# Press Enter for default location
# Set passphrase (optional)

# Copy public key
cat ~/.ssh/id_ed25519.pub
```

**Add to GitHub:**
1. Go to GitHub → Settings → SSH and GPG keys
2. Click **"New SSH key"**
3. Paste public key
4. Click **"Add SSH key"**

**Change remote to SSH:**
```bash
git remote set-url origin git@github.com:leviceroy/SWR_Monte_Carlo.git

# Verify
git remote -v

# Push
git push -u origin main
```

---

## ✅ Step 5: Verify on GitHub

**Visit your repository:**
```
https://github.com/leviceroy/SWR_Monte_Carlo
```

**You should see:**
- ✅ README.md displayed on homepage
- ✅ All files present
- ✅ Green "Code" button (can clone)
- ✅ Commit history

---

## 🏷️ Step 6: Add Releases (Optional)

**Create first release:**

1. Go to repository page → **"Releases"** (right sidebar)
2. Click **"Create a new release"**
3. Configure:
   ```
   Tag version: v3.2
   Release title: v3.2 - Latest Release
   Description:

   ## SWR Monte Carlo Simulator v3.2

   **Features:**
   - 4 portfolio presets (Dividend, Three-Fund, Golden Butterfly, Modern)
   - Geometric returns with annual rebalancing
   - Fat-tail mode for black swan modeling
   - Investment fee modeling (expense ratios + advisor fees)
   - Docker support for easy deployment
   - Comprehensive documentation

   **Quick Start:**
   ```bash
   git clone https://github.com/leviceroy/SWR_Monte_Carlo.git
   cd SWR_Monte_Carlo
   docker-compose run --rm swr-monte-carlo
   ```

   **Documentation:**
   - [README.md](README.md) - Main documentation
   - [DOCKER_SETUP.md](DOCKER_SETUP.md) - Docker guide
   - [ReadME_V3.md](ReadME_V3.md) - Technical details
   ```

4. Click **"Publish release"**

---

## 📋 Step 7: Add LICENSE File

**Create MIT License:**

```bash
cd "/home/shinybunny/Pythonscripts/Monte/MonteCarlo Sim"
```

Create `LICENSE` file:
```
MIT License

Copyright (c) 2024 leviceroy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

**Commit and push:**
```bash
git add LICENSE
git commit -m "Add MIT License"
git push
```

---

## 🎨 Step 8: Customize Repository Settings

**Go to Settings (repository page):**

### General
- ✅ Check "Include in the GitHub Archive Program"
- ✅ Check "Automatically delete head branches" (clean up after PRs)

### Features
- ✅ Wikis (for additional documentation)
- ✅ Issues (for bug reports/feature requests)
- ✅ Projects (for roadmap tracking)
- ❌ Sponsorships (unless you want donations)

### Social Preview
Upload a preview image (optional):
- Create image: 1280x640 px
- Show calculator output or logo
- Upload in Settings → Social preview

---

## 📊 Step 9: Add Topics/Tags

**Add topics** for discoverability:

Repository page → ⚙️ (settings icon next to "About")

**Suggested topics:**
```
monte-carlo
retirement-planning
safe-withdrawal-rate
bogleheads
portfolio-optimization
fire-movement
financial-independence
python
docker
finance-calculator
investment-analysis
```

**Add website** (if you have blog post):
```
https://yourblog.com/monte-carlo-calculator
```

---

## 🔄 Step 10: Regular Workflow

### Making Changes

```bash
# 1. Make changes to files
vim SWR_Monte_Carlo.py

# 2. Check what changed
git status
git diff

# 3. Stage changes
git add SWR_Monte_Carlo.py

# 4. Commit
git commit -m "Fix: Correct correlation matrix for Portfolio 3"

# 5. Push to GitHub
git push
```

---

### Creating Branches for Features

```bash
# Create and switch to new branch
git checkout -b feature/add-tax-modeling

# Make changes...
git add .
git commit -m "Add tax modeling for US investors"

# Push branch
git push -u origin feature/add-tax-modeling

# Create Pull Request on GitHub
# Merge when ready
```

---

### Updating from Main

```bash
# Switch to main
git checkout main

# Pull latest changes
git pull

# Switch back to feature branch
git checkout feature/add-tax-modeling

# Merge main into feature
git merge main
```

---

## 🌟 Step 11: Promote Your Repository

### Add Badges to README

**Already in README.md:**
```markdown
[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](Dockerfile)
```

**Additional badges** (optional):
```markdown
[![GitHub stars](https://img.shields.io/github/stars/leviceroy/SWR_Monte_Carlo?style=social)](https://github.com/leviceroy/SWR_Monte_Carlo)
[![GitHub forks](https://img.shields.io/github/forks/leviceroy/SWR_Monte_Carlo?style=social)](https://github.com/leviceroy/SWR_Monte_Carlo/fork)
[![GitHub issues](https://img.shields.io/github/issues/leviceroy/SWR_Monte_Carlo)](https://github.com/leviceroy/SWR_Monte_Carlo/issues)
```

---

### Share on Social Media

**Reddit:**
- r/financialindependence
- r/Bogleheads
- r/Fire
- r/investing

**Bogleheads Forum:**
- https://www.bogleheads.org/forum/

**Hacker News:**
- https://news.ycombinator.com/submit

**Twitter/X:**
```
🚀 Just open-sourced my Monte Carlo retirement simulator!

✅ 4 portfolio strategies
✅ Safe Withdrawal Rate analysis
✅ Docker support
✅ 100% free & open source

Perfect for #FIRE #Bogleheads #RetirementPlanning

https://github.com/leviceroy/SWR_Monte_Carlo
```

---

## 🔧 Maintenance

### Keeping Dependencies Updated

```bash
# Check for outdated packages
pip list --outdated

# Update requirements.txt
pip freeze > requirements.txt

# Commit
git add requirements.txt
git commit -m "Update dependencies"
git push
```

---

### Responding to Issues

**When users report bugs:**
1. Reproduce the issue
2. Create branch: `git checkout -b fix/issue-123`
3. Fix the bug
4. Test thoroughly
5. Commit: `git commit -m "Fix #123: Correct percentile calculation"`
6. Push and create PR
7. Merge when ready
8. Close issue with comment

---

### Versioning Strategy

**Semantic Versioning (SemVer):**
- `v3.0.0` - Major version (breaking changes)
- `v3.1.0` - Minor version (new features, backward compatible)
- `v3.0.1` - Patch version (bug fixes)

**Creating new version:**
```bash
# Make changes
git add .
git commit -m "Add variable withdrawal strategy"

# Tag
git tag v3.1.0
git push origin v3.1.0

# Create release on GitHub
```

---

## 📚 Additional GitHub Features

### GitHub Actions (CI/CD)

Create `.github/workflows/test.yml`:
```yaml
name: Test

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: pip install -r requirements.txt
      - name: Run tests
        run: python -m pytest tests/
```

---

### GitHub Pages (Documentation Site)

1. Create `docs/` directory
2. Add documentation
3. Settings → Pages → Source: `main` branch, `/docs` folder
4. Site published at: `https://leviceroy.github.io/SWR_Monte_Carlo/`

---

### GitHub Discussions

Enable in Settings → Features → Discussions

**Use for:**
- Q&A
- Feature requests
- General discussion
- Sharing results

---

## ✅ Final Checklist

- [ ] Repository created on GitHub
- [ ] Local Git initialized
- [ ] All files committed
- [ ] Pushed to GitHub
- [ ] README displays correctly
- [ ] LICENSE added
- [ ] .gitignore working (outputs/ not tracked)
- [ ] Topics/tags added
- [ ] Release v3.2 created
- [ ] Repository settings configured
- [ ] Shared on social media (optional)

---

## 🆘 Troubleshooting

### "Fatal: remote origin already exists"

```bash
git remote rm origin
git remote add origin https://github.com/leviceroy/SWR_Monte_Carlo.git
```

---

### "Permission denied (publickey)"

**Using HTTPS instead:**
```bash
git remote set-url origin https://github.com/leviceroy/SWR_Monte_Carlo.git
```

---

### "Updates were rejected because the remote contains work"

```bash
# Pull first
git pull origin main --rebase

# Then push
git push
```

---

### "Large files detected"

GitHub has 100MB file limit.

**Solution:**
```bash
# Add to .gitignore
echo "large_file.csv" >> .gitignore

# Remove from Git (keep local copy)
git rm --cached large_file.csv

# Commit
git commit -m "Remove large file from tracking"
```

---

**GitHub setup complete!** 🎉

Your repository is now live at:
```
https://github.com/leviceroy/SWR_Monte_Carlo
```

Return to [README.md](README.md) for usage documentation.
