#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

clear
echo -e "${BLUE}"
echo "================================================================================"
echo "              Inventory Management System - Automated Setup"
echo "================================================================================"
echo -e "${NC}\n"

# Check if Python is installed
if ! command -v python3 &> /dev/null && ! command -v python &> /dev/null; then
    echo -e "${RED}❌ Python is not installed!${NC}"
    echo -e "Please install Python 3.8 or higher from: https://www.python.org/downloads/"
    exit 1
fi

# Use python3 if available, otherwise python
if command -v python3 &> /dev/null; then
    PYTHON=python3
else
    PYTHON=python
fi

echo -e "${BLUE}Using Python:${NC} $($PYTHON --version)"
echo ""

# Step 1: Virtual Environment
echo -e "${BLUE}[1/6] Creating virtual environment...${NC}"
$PYTHON -m venv venv
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to create virtual environment${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Virtual environment created${NC}\n"

# Step 2: Activate
echo -e "${BLUE}[2/6] Activating virtual environment...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Virtual environment activated${NC}\n"

# Step 3: Install Dependencies
echo -e "${BLUE}[3/6] Installing dependencies...${NC}"
pip install --upgrade pip -q
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to install dependencies${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Dependencies installed${NC}\n"

# Step 4: Create Migrations
echo -e "${BLUE}[4/6] Creating database migrations...${NC}"
python manage.py makemigrations homepage
python manage.py makemigrations inventory
python manage.py makemigrations transactions
echo -e "${GREEN}✓ Migrations created${NC}\n"

# Step 5: Apply Migrations (CRITICAL!)
echo -e "${BLUE}[5/6] Applying migrations to database...${NC}"
echo -e "${YELLOW}⚠ This step is CRITICAL - creates all database tables${NC}"
python manage.py migrate
if [ $? -ne 0 ]; then
    echo -e "${RED}❌ Failed to apply migrations${NC}"
    exit 1
fi
echo -e "${GREEN}✓ Database tables created successfully${NC}\n"

# Step 6: Demo Data
echo -e "${BLUE}[6/6] Loading demo data...${NC}"
python populate_data.py
if [ $? -ne 0 ]; then
    echo -e "${YELLOW}⚠ Demo data loading had issues, but database is ready${NC}"
    echo -e "${YELLOW}  You can still use the system - just register a new account${NC}\n"
else
    echo -e "${GREEN}✓ Demo data loaded successfully${NC}\n"
fi

# Success Message
echo -e "${GREEN}"
echo "================================================================================"
echo "                         ✓ SETUP COMPLETED SUCCESSFULLY!"
echo "================================================================================"
echo -e "${NC}\n"

echo -e "${BLUE}Demo Admin Account (if demo data loaded):${NC}"
echo -e "  Email:    ${YELLOW}admin@example.com${NC}"
echo -e "  Password: ${YELLOW}admin123${NC}\n"

echo -e "${BLUE}To start the server:${NC}"
echo -e "  ${YELLOW}source venv/bin/activate${NC}  (activate virtual environment)"
echo -e "  ${YELLOW}python manage.py runserver${NC}  (start server)\n"

echo -e "${BLUE}Then open in browser:${NC}"
echo -e "  ${YELLOW}http://127.0.0.1:8000${NC}\n"

echo -e "${GREEN}Options to login:${NC}"
echo -e "  1. Register a new account (click 'Sign up')"
echo -e "  2. Use demo admin (if populated)${NC}\n"

echo -e "${YELLOW}Press Enter to continue...${NC}"
read
