# Docker Setup Guide - SWR Monte Carlo Simulator

Complete guide for running the Monte Carlo Retirement Simulator in Docker.

---

## 📦 Why Docker?

**Benefits:**
- ✅ No Python installation required
- ✅ No dependency conflicts
- ✅ Works identically on Windows/Mac/Linux
- ✅ One-command setup
- ✅ Isolated environment
- ✅ Easy to share and deploy

---

## 🚀 Quick Start (TL;DR)

```bash
# 1. Install Docker (see below for OS-specific instructions)
# 2. Clone repository
git clone https://github.com/leviceroy/SWR_Monte_Carlo.git
cd SWR_Monte_Carlo

# 3. Run simulation
docker-compose run --rm swr-monte-carlo

# That's it! 🎉
```

---

## 📥 Installing Docker

### Windows 10/11

**1. Download Docker Desktop:**
- Visit: https://www.docker.com/products/docker-desktop
- Download Docker Desktop for Windows
- Run installer

**2. System Requirements:**
- Windows 10 64-bit: Pro, Enterprise, or Education (Build 19041+)
- OR Windows 11
- Enable WSL 2 (Windows Subsystem for Linux)

**3. Enable WSL 2:**
```powershell
# Run in PowerShell as Administrator
wsl --install
wsl --set-default-version 2
```

**4. Verify Installation:**
```powershell
docker --version
docker-compose --version
```

**Expected Output:**
```
Docker version 24.0.x, build xxxxx
Docker Compose version v2.x.x
```

---

### macOS

**1. Download Docker Desktop:**
- Visit: https://www.docker.com/products/docker-desktop
- Download Docker Desktop for Mac (Intel or Apple Silicon)
- Drag to Applications folder

**2. System Requirements:**
- macOS 11 Big Sur or newer
- 4GB RAM minimum

**3. Verify Installation:**
```bash
docker --version
docker-compose --version
```

---

### Linux (Ubuntu/Debian)

**1. Install Docker Engine:**
```bash
# Update package index
sudo apt-get update

# Install dependencies
sudo apt-get install -y \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

**2. Post-Installation (Run Docker without sudo):**
```bash
# Add your user to docker group
sudo usermod -aG docker $USER

# Log out and back in (or reboot)
newgrp docker
```

**3. Verify Installation:**
```bash
docker --version
docker compose version  # Note: 'compose' not 'docker-compose' on newer versions
```

---

## 🏗️ Building the Docker Image

### Using Docker Compose (Recommended)

Docker Compose will automatically build the image on first run:

```bash
# Navigate to project directory
cd SWR_Monte_Carlo

# Build image (optional - happens automatically on first run)
docker-compose build

# View built images
docker images | grep swr-monte-carlo
```

**Output:**
```
REPOSITORY          TAG       IMAGE ID       CREATED         SIZE
swr-monte-carlo     latest    abc123def456   2 minutes ago   450MB
```

---

### Using Docker CLI (Manual)

```bash
# Build image manually
docker build -t swr-monte-carlo:latest .

# Verify image
docker images swr-monte-carlo
```

---

## 🎯 Running Simulations

### Method 1: Docker Compose (Easiest)

**Default simulation (Portfolio 2, 3% withdrawal, 50 years):**
```bash
docker-compose run --rm swr-monte-carlo
```

**Custom parameters:**
```bash
docker-compose run --rm swr-monte-carlo python SWR_Monte_Carlo.py \
  --portfolio 3 \
  --initial-value 1500000 \
  --withdrawal-rate 3.5 \
  --years 40 \
  --simulations 50000 \
  --fat-tails
```

**Interactive mode (enter container):**
```bash
docker-compose run --rm swr-monte-carlo /bin/bash

# Now inside container:
python SWR_Monte_Carlo.py --portfolio 1
python SWR_Monte_Carlo.py --portfolio 2 --fat-tails
exit
```

---

### Method 2: Docker CLI (Manual)

**Run with default parameters:**
```bash
docker run --rm -v $(pwd)/outputs:/app/outputs swr-monte-carlo:latest \
  python SWR_Monte_Carlo.py --portfolio 2
```

**Run with custom parameters:**
```bash
docker run --rm -v $(pwd)/outputs:/app/outputs swr-monte-carlo:latest \
  python SWR_Monte_Carlo.py \
  --portfolio 3 \
  --withdrawal-rate 4.0 \
  --fat-tails
```

**Enter container interactively:**
```bash
docker run --rm -it -v $(pwd)/outputs:/app/outputs swr-monte-carlo:latest /bin/bash
```

---

## 📂 Volume Mounting (Persisting Outputs)

Docker containers are **ephemeral** - files created inside are lost when container stops.

**Solution:** Mount `outputs/` directory to persist CSV results.

### Automatic (Docker Compose)

```yaml
# Already configured in docker-compose.yml
volumes:
  - ./outputs:/app/outputs
```

**Usage:**
```bash
docker-compose run --rm swr-monte-carlo

# Results saved to ./outputs/ on your host machine
ls -lh outputs/
```

---

### Manual (Docker CLI)

**Linux/macOS:**
```bash
docker run --rm -v $(pwd)/outputs:/app/outputs swr-monte-carlo:latest \
  python SWR_Monte_Carlo.py --portfolio 2
```

**Windows (PowerShell):**
```powershell
docker run --rm -v ${PWD}/outputs:/app/outputs swr-monte-carlo:latest `
  python SWR_Monte_Carlo.py --portfolio 2
```

**Windows (Command Prompt):**
```cmd
docker run --rm -v %cd%/outputs:/app/outputs swr-monte-carlo:latest ^
  python SWR_Monte_Carlo.py --portfolio 2
```

---

## 🔧 Customizing docker-compose.yml

Edit `docker-compose.yml` to change default parameters:

```yaml
services:
  swr-monte-carlo:
    build: .
    volumes:
      - ./outputs:/app/outputs
    command: >
      python SWR_Monte_Carlo.py
      --portfolio 2              # ← Change default portfolio
      --withdrawal-rate 3.5      # ← Change withdrawal rate
      --simulations 50000        # ← Change simulation count
      --fat-tails                # ← Enable by default
```

**Then run:**
```bash
docker-compose run --rm swr-monte-carlo
```

---

## 🧹 Cleanup Commands

### Remove Stopped Containers

```bash
# List all containers
docker ps -a

# Remove specific container
docker rm <container-id>

# Remove all stopped containers
docker container prune -f
```

---

### Remove Images

```bash
# List images
docker images

# Remove specific image
docker rmi swr-monte-carlo:latest

# Remove all unused images
docker image prune -a -f
```

---

### Complete Cleanup (Nuclear Option)

```bash
# Stop and remove everything (containers, networks, volumes, images)
docker-compose down --volumes --rmi all

# Remove ALL Docker data (use with caution!)
docker system prune -a --volumes -f
```

---

## 🐛 Troubleshooting

### Issue 1: "Cannot connect to Docker daemon"

**Error:**
```
Cannot connect to the Docker daemon at unix:///var/run/docker.sock
```

**Solution:**
```bash
# Start Docker service (Linux)
sudo systemctl start docker

# Or restart Docker Desktop (Windows/Mac)
# Open Docker Desktop application
```

---

### Issue 2: "Permission denied" on Linux

**Error:**
```
Got permission denied while trying to connect to the Docker daemon socket
```

**Solution:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Log out and back in (or run):
newgrp docker

# Verify
docker ps
```

---

### Issue 3: "Port already in use"

**Error:**
```
Bind for 0.0.0.0:8080 failed: port is already allocated
```

**Solution:**
```bash
# Find process using port
sudo lsof -i :8080

# Kill process
sudo kill -9 <PID>

# Or change port in docker-compose.yml
```

---

### Issue 4: Build fails with "no space left on device"

**Solution:**
```bash
# Clean up Docker
docker system prune -a --volumes -f

# Check disk space
df -h
```

---

### Issue 5: Outputs not persisting

**Problem:** CSV files disappear after container stops

**Solution:**
```bash
# Verify volume mount
docker inspect <container-id> | grep Mounts -A 10

# Check outputs directory exists
mkdir -p outputs

# Ensure correct permissions (Linux)
chmod 755 outputs
```

---

### Issue 6: Slow performance on Windows

**Problem:** Docker runs slowly on Windows

**Solution:**
```bash
# 1. Ensure WSL 2 is enabled (not WSL 1)
wsl --set-default-version 2

# 2. Move project to WSL filesystem (faster)
# Instead of: C:\Users\YourName\SWR_Monte_Carlo
# Use: \\wsl$\Ubuntu\home\yourname\SWR_Monte_Carlo

# 3. Increase Docker Desktop resources
# Settings → Resources → Advanced → Increase CPU/RAM
```

---

## 🎓 Advanced Usage

### Running Multiple Simulations in Parallel

```bash
# Create a script: run_batch.sh
#!/bin/bash

for portfolio in {1..4}; do
  for rate in 2.5 3.0 3.5 4.0; do
    echo "Running Portfolio $portfolio at $rate% withdrawal..."
    docker-compose run --rm swr-monte-carlo python SWR_Monte_Carlo.py \
      --portfolio $portfolio \
      --withdrawal-rate $rate \
      --simulations 10000
  done
done

echo "Batch complete! Check outputs/ directory"
```

**Run:**
```bash
chmod +x run_batch.sh
./run_batch.sh
```

---

### Using Different Python Versions

**Modify Dockerfile:**
```dockerfile
# Change first line
FROM python:3.11-slim  # ← Change to 3.9, 3.10, 3.12, etc.
```

**Rebuild:**
```bash
docker-compose build --no-cache
```

---

### Debugging Inside Container

```bash
# Enter container with bash
docker-compose run --rm swr-monte-carlo /bin/bash

# Now inside container - explore:
ls -la
cat SWR_Monte_Carlo.py
python --version
pip list

# Test manually
python SWR_Monte_Carlo.py --portfolio 1

# Exit
exit
```

---

### Using Custom Data Files

**Mount additional files:**

```yaml
# docker-compose.yml
volumes:
  - ./outputs:/app/outputs
  - ./custom_data.csv:/app/custom_data.csv  # ← Add custom files
```

---

## 📊 Comparing Results

### Run Same Simulation Locally vs Docker

**Local Python:**
```bash
source venv/bin/activate
python SWR_Monte_Carlo.py --portfolio 2 --simulations 10000
```

**Docker:**
```bash
docker-compose run --rm swr-monte-carlo python SWR_Monte_Carlo.py \
  --portfolio 2 --simulations 10000
```

**Results should be identical** (within Monte Carlo randomness).

---

## 🔐 Security Considerations

### Running as Non-Root User (Recommended)

**Add to Dockerfile:**
```dockerfile
# After WORKDIR /app
RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser
```

**Rebuild:**
```bash
docker-compose build --no-cache
```

---

### Scanning Image for Vulnerabilities

```bash
# Install Trivy (vulnerability scanner)
# Linux:
sudo apt-get install wget
wget https://github.com/aquasecurity/trivy/releases/download/v0.18.3/trivy_0.18.3_Linux-64bit.deb
sudo dpkg -i trivy_0.18.3_Linux-64bit.deb

# Scan image
trivy image swr-monte-carlo:latest
```

---

## 🌐 Deploying to Cloud

### Docker Hub

```bash
# Tag image
docker tag swr-monte-carlo:latest yourusername/swr-monte-carlo:latest

# Login
docker login

# Push
docker push yourusername/swr-monte-carlo:latest

# Others can now pull:
docker pull yourusername/swr-monte-carlo:latest
```

---

### AWS ECS / Azure Container Instances / Google Cloud Run

See respective platform documentation for deploying Docker containers.

**Basic pattern:**
1. Push image to container registry (Docker Hub, ECR, GCR, ACR)
2. Create container service
3. Configure environment variables
4. Set volume mounts for outputs
5. Deploy

---

## 📚 Additional Resources

**Official Documentation:**
- Docker Docs: https://docs.docker.com/
- Docker Compose: https://docs.docker.com/compose/
- Docker Hub: https://hub.docker.com/

**Tutorials:**
- Docker Getting Started: https://docs.docker.com/get-started/
- Docker Compose Tutorial: https://docs.docker.com/compose/gettingstarted/

**Community:**
- Docker Community: https://www.docker.com/community/
- Stack Overflow: https://stackoverflow.com/questions/tagged/docker

---

## ✅ Checklist for New Users

- [ ] Docker Desktop installed and running
- [ ] Repository cloned: `git clone https://github.com/leviceroy/SWR_Monte_Carlo.git`
- [ ] Navigated to directory: `cd SWR_Monte_Carlo`
- [ ] Built image (optional): `docker-compose build`
- [ ] Ran first simulation: `docker-compose run --rm swr-monte-carlo`
- [ ] Verified outputs: `ls -lh outputs/`
- [ ] Read main README.md for usage examples

---

## 🆘 Still Having Issues?

1. **Check Docker is running:**
   ```bash
   docker ps
   ```

2. **Verify files exist:**
   ```bash
   ls -la
   # Should see: Dockerfile, docker-compose.yml, SWR_Monte_Carlo.py
   ```

3. **Try clean rebuild:**
   ```bash
   docker-compose down
   docker-compose build --no-cache
   docker-compose run --rm swr-monte-carlo
   ```

4. **Check Docker logs:**
   ```bash
   docker-compose logs
   ```

5. **Open GitHub issue** with:
   - Operating system and version
   - Docker version (`docker --version`)
   - Error message (full output)
   - Steps to reproduce

---

**Docker setup complete!** 🐳

Return to [README.md](README.md) for usage examples and documentation.
