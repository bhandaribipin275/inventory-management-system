@echo off
REM Quick run script - assumes setup already done

echo Starting Inventory Management System...
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Virtual environment not found! Please run setup.bat first.
    pause
    exit /b 1
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Check if database exists
if not exist "db.sqlite3" (
    echo Database not found! Running migrations...
    python manage.py migrate
    echo.
    echo Database created. You can now register a new account or run populate_data.py for demo data.
    echo.
)

REM Start server
echo Starting development server...
echo Open http://127.0.0.1:8000 in your browser
echo Press Ctrl+C to stop the server
echo.
python manage.py runserver
