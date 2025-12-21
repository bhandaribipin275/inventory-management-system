#!/bin/bash
# Quick run script - assumes setup already done

echo "Starting Inventory Management System..."
echo ""

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "Virtual environment not found! Please run setup.sh first."
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Check if database exists
if [ ! -f "db.sqlite3" ]; then
    echo "Database not found! Running migrations..."
    python manage.py migrate
    echo ""
    echo "Database created. You can now register a new account or run populate_data.py for demo data."
    echo ""
fi

# Start server
echo "Starting development server..."
echo "Open http://127.0.0.1:8000 in your browser"
echo "Press Ctrl+C to stop the server"
echo ""
python manage.py runserver
