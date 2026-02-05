#!/bin/bash

# Smart City ML Platform - Setup and Run Script
# This script automates the setup and deployment process

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔════════════════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║   Smart City ML Platform - Setup Script                ║${NC}"
echo -e "${BLUE}╚════════════════════════════════════════════════════════╝${NC}"
echo ""

# Check Python version
echo -e "${YELLOW}[1/6] Checking Python version...${NC}"
python_version=$(python --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python version: $python_version${NC}"

# Create virtual environment
echo -e "${YELLOW}[2/6] Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python -m venv venv
    echo -e "${GREEN}✓ Virtual environment created${NC}"
else
    echo -e "${GREEN}✓ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}[3/6] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}"

# Install dependencies
echo -e "${YELLOW}[4/6] Installing dependencies...${NC}"
pip install --upgrade pip setuptools wheel > /dev/null 2>&1
pip install -r requirements.txt > /dev/null 2>&1
echo -e "${GREEN}✓ Dependencies installed${NC}"

# Train models
echo -e "${YELLOW}[5/6] Training ML models...${NC}"
if [ ! -d "models" ]; then
    mkdir -p models
fi
if [ ! -f "models/air_quality_random_forest.pkl" ]; then
    python train_models.py
    echo -e "${GREEN}✓ Models trained successfully${NC}"
else
    echo -e "${GREEN}✓ Models already exist${NC}"
fi

# Start services
echo -e "${YELLOW}[6/6] Starting services...${NC}"
echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}Setup completed successfully!${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""

# Display next steps
echo -e "${BLUE}Next steps:${NC}"
echo ""
echo -e "${YELLOW}Option 1: Run locally with separate terminals${NC}"
echo "  Terminal 1 - API Server:"
echo -e "    ${BLUE}cd Smart_City_ML_Project && python -m uvicorn backend.main:app --reload${NC}"
echo ""
echo "  Terminal 2 - Dashboard:"
echo -e "    ${BLUE}cd Smart_City_ML_Project && streamlit run dashboard/app.py${NC}"
echo ""

echo -e "${YELLOW}Option 2: Run with Docker Compose${NC}"
echo -e "    ${BLUE}docker-compose up --build${NC}"
echo ""

echo -e "${YELLOW}Access the application:${NC}"
echo -e "  API Docs: ${BLUE}http://localhost:8000/api/docs${NC}"
echo -e "  Dashboard: ${BLUE}http://localhost:8501${NC}"
echo ""

echo -e "${YELLOW}Documentation:${NC}"
echo -e "  README: See README.md"
echo -e "  Deployment Guide: See DEPLOYMENT.md"
echo -e "  API Reference: http://localhost:8000/api/docs (after starting API)"
echo ""
