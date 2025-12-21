# Inventory Management System

A complete Django-based inventory management system with user authentication, stock tracking, purchases, sales, and real-time analytics.

![Django](https://img.shields.io/badge/Django-4.x-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3-purple)

---

## 🚀 Quick Start (3 Steps!)

### Windows
```bash
1. setup.bat          # Run this once
2. run.bat            # Start server (or: python manage.py runserver)
3. Open: http://127.0.0.1:8000
```

### Mac/Linux
```bash
1. chmod +x setup.sh && ./setup.sh    # Run this once
2. ./run.sh                           # Start server (or: python manage.py runserver)
3. Open: http://127.0.0.1:8000
```

**First time?** Read **QUICK-START.txt** for detailed instructions!

---

## ✨ Features

- ✅ **User Registration & Login** - Secure authentication system
- 📊 **Real-time Dashboard** - Statistics, charts, and activity tracking
- 📦 **Stock Management** - Track inventory with SKU, categories, suppliers
- 🛒 **Purchase Orders** - Record incoming stock with automatic updates
- 💰 **Sales Transactions** - Process sales with stock validation
- 📈 **Stock History** - Complete audit trail of all movements
- ⚠️ **Low Stock Alerts** - Visual warnings for items below reorder level
- 👥 **Multi-user Support** - Role-based access control

---

## 📋 What the Setup Does

The `setup.bat` or `setup.sh` script automatically:

1. ✅ Creates a Python virtual environment
2. ✅ Installs all required packages
3. ✅ Creates database migrations
4. ✅ **Applies migrations** (creates database tables) ← **CRITICAL!**
5. ✅ Loads demo data with sample products and admin account
6. ✅ Sets everything up ready to run

**⚠️ IMPORTANT:** If you skip the setup script and run manually, you **MUST** run migrations:
```bash
python manage.py migrate
```
Otherwise you'll get "no such table" errors!

---

## 🔑 Login After Setup

### Option 1: Register New Account (Recommended)
1. Go to http://127.0.0.1:8000
2. Click **"Sign up"**
3. Create your account
4. Login

### Option 2: Use Demo Admin
After running the setup script (which runs `populate_data.py`):
- **Email:** admin@example.com
- **Password:** admin123

---

## 🛠️ Manual Setup (If Setup Script Fails)

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# 3. Install packages
pip install -r requirements.txt

# 4. CRITICAL: Run migrations (creates database)
python manage.py migrate

# 5. (Optional) Load demo data
python populate_data.py

# 6. Start server
python manage.py runserver
```

---

## 📁 Project Structure

```
inventory-management-system/
├── 📄 QUICK-START.txt         # Read this first!
├── 📄 README.md               # This file
├── 🔧 setup.bat / setup.sh    # One-time setup
├── ▶️ run.bat / run.sh        # Quick start server
├── 📋 requirements.txt        # Python packages
├── 🗄️ db.sqlite3             # Database (created by migrations)
├── 🔧 manage.py               # Django management
├── 📊 populate_data.py        # Demo data loader
│
├── 📁 core/                   # Project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── 📁 homepage/               # Authentication & Dashboard
│   ├── views.py              # Login, Register, Dashboard
│   ├── models.py             # UserProfile, ActivityLog
│   ├── urls.py
│   └── migrations/           # Database migrations
│
├── 📁 inventory/              # Stock Management
│   ├── views.py              # Stock CRUD operations
│   ├── models.py             # Category, Supplier, Stock, History
│   ├── urls.py
│   └── migrations/
│
├── 📁 transactions/           # Purchases & Sales
│   ├── views.py              # Transaction processing
│   ├── models.py             # Purchase, Sale, Items
│   ├── urls.py
│   └── migrations/
│
└── 📁 templates/              # HTML templates
    ├── base.html
    ├── homepage/
    ├── inventory/
    └── transactions/
```

---

## 🗄️ Database

The system uses **SQLite** (no installation required). The database file `db.sqlite3` is created automatically when you run migrations.

**Tables created:**
- Users and authentication
- User profiles
- Categories, Suppliers, Stock items
- Stock history (audit trail)
- Purchases and Sales with line items
- Activity logs

**Everything persists** - your data is saved automatically!

---

## 🚨 Troubleshooting

### Error: "no such table: auth_user"
**Cause:** You didn't run migrations  
**Fix:** Run `python manage.py migrate`

### Error: "18 unapplied migrations"
**Cause:** Database tables not created  
**Fix:** Run `python manage.py migrate`

### Error: Port already in use
**Fix:** Use a different port: `python manage.py runserver 8080`

### Static files warning
**Fix:** Create a `static` folder (warning is harmless, won't affect functionality)

---

## 💻 Tech Stack

- **Backend:** Django 4.2.7, Python 3.8+
- **Database:** SQLite (built-in)
- **Frontend:** Bootstrap 5.3, Bootstrap Icons
- **Charts:** Chart.js 4.4
- **Fonts:** Google Fonts (Inter)

---

## 📖 Usage Guide

### Dashboard
- View total items, categories, suppliers
- See purchase and sales statistics
- Monitor 7-day stock activity chart
- Check low stock alerts
- Review recent transactions

### Stock Management
- Add/Edit/Delete products
- Organize by categories
- Track suppliers
- Set reorder levels
- Manual stock adjustments (IN/OUT)
- View complete stock history

### Purchases
- Create purchase orders
- Add multiple items per order
- Automatic stock quantity updates
- Track supplier information

### Sales
- Process customer orders
- Stock validation before sale
- Automatic inventory deduction
- Transaction history

---

## 🔐 Security

- ✅ Password validation (min 6 characters)
- ✅ Email uniqueness enforcement
- ✅ CSRF protection on all forms
- ✅ Login required for all operations
- ✅ Secure password hashing (Django default)

---

## 🎯 Next Steps

1. **Run setup script** (setup.bat or setup.sh)
2. **Start server** (run.bat or run.sh)
3. **Register account** or use demo login
4. **Explore dashboard**
5. **Add categories** and **suppliers**
6. **Create products**
7. **Record purchases** and **sales**
8. **Monitor stock levels**

---

## 📝 License

MIT License - Free for personal and commercial use

---

## 💡 Tips

- Use the demo account to explore features before registering
- The dashboard shows the last 7 days of activity
- Low stock items (below reorder level) appear with warnings
- All stock movements are tracked in history for auditing
- You can adjust stock manually for corrections
- Delete transactions to reverse stock changes

---

## 🆘 Need Help?

1. Read **QUICK-START.txt**
2. Check **Troubleshooting** section above
3. Make sure you ran `python manage.py migrate`
4. Verify virtual environment is activated
5. Check Python version is 3.8 or higher

---

**That's it! Happy inventory managing! 📦**
