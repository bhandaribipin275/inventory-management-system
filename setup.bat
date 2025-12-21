@echo off
cls
echo ================================================================================
echo              Inventory Management System - Automated Setup
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python is not installed!
    echo Please install Python 3.8 or higher from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo Using Python:
python --version
echo.

REM Step 1: Virtual Environment
echo [1/6] Creating virtual environment...
python -m venv venv
if errorlevel 1 (
    echo [ERROR] Failed to create virtual environment
    pause
    exit /b 1
)
echo [OK] Virtual environment created
echo.

REM Step 2: Activate
echo [2/6] Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Step 3: Install Dependencies
echo [3/6] Installing dependencies...
python -m pip install --upgrade pip >nul 2>&1
pip install -r requirements.txt
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    pause
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Step 4: Create Migrations
echo [4/6] Creating database migrations...
python manage.py makemigrations homepage
python manage.py makemigrations inventory
python manage.py makemigrations transactions
echo [OK] Migrations created
echo.

REM Step 5: Apply Migrations (CRITICAL!)
echo [5/6] Applying migrations to database...
echo [WARNING] This step is CRITICAL - creates all database tables
python manage.py migrate
if errorlevel 1 (
    echo [ERROR] Failed to apply migrations
    pause
    exit /b 1
)
echo [OK] Database tables created successfully
echo.

REM Step 6: Demo Data
echo [6/6] Loading demo data...
python populate_data.py
if errorlevel 1 (
    echo [WARNING] Demo data loading had issues, but database is ready
    echo           You can still use the system - just register a new account
    echo.
) else (
    echo [OK] Demo data loaded successfully
    echo.
)

REM Success Message
echo ================================================================================
echo                         [SUCCESS] SETUP COMPLETED!
echo ================================================================================
echo.

echo Demo Admin Account (if demo data loaded):
echo   Email:    admin@example.com
echo   Password: admin123
echo.

echo To start the server:
echo   venv\Scripts\activate  (activate virtual environment)
echo   python manage.py runserver  (start server)
echo.

echo Then open in browser:
echo   http://127.0.0.1:8000
echo.

echo Options to login:
echo   1. Register a new account (click 'Sign up')
echo   2. Use demo admin (if populated)
echo.

pause
