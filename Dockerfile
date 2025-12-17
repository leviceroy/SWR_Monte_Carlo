# SWR Monte Carlo Retirement Simulator
# Docker Image for Easy Deployment
# =====================================

FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies (minimal)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY SWR_Monte_Carlo.py .
COPY README.md .
COPY ReadME_V3.md .

# Create outputs directory
RUN mkdir -p outputs

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Default command shows help
CMD ["python", "SWR_Monte_Carlo.py", "--help"]
