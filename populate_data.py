#!/usr/bin/env python
"""
Populate database with demo data for the Inventory Management System.
Run with: python populate_data.py
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from inventory.models import Category, Supplier, Stock, StockHistory
from transactions.models import Purchase, PurchaseItem, Sale, SaleItem
from datetime import date, timedelta
from decimal import Decimal
import random

# Try to import optional models
try:
    from homepage.models import UserProfile, ActivityLog
    HAS_HOMEPAGE_MODELS = True
except ImportError:
    HAS_HOMEPAGE_MODELS = False

def create_admin_user():
    """Create admin user"""
    print("Creating admin user...")
    
    # Delete existing admin if exists
    User.objects.filter(username='admin@example.com').delete()
    
    admin = User.objects.create_superuser(
        username='admin@example.com',
        email='admin@example.com',
        password='admin123',
        first_name='Admin',
        last_name='User'
    )
    
    if HAS_HOMEPAGE_MODELS:
        try:
            UserProfile.objects.create(
                user=admin,
                role='admin',
                phone='+1-555-0100',
                address='123 Admin St, New York, NY 10001'
            )
        except Exception as e:
            print(f"  Note: Could not create user profile: {e}")
    
    print(f"  ✓ Created admin user: {admin.email}")
    return admin

def create_categories():
    """Create product categories"""
    print("Creating categories...")
    
    categories_data = [
        {'name': 'Electronics', 'description': 'Electronic devices and accessories'},
        {'name': 'Furniture', 'description': 'Office and home furniture'},
        {'name': 'Stationery', 'description': 'Office supplies and stationery'},
        {'name': 'Hardware', 'description': 'Hardware tools and equipment'},
        {'name': 'Software', 'description': 'Software licenses and subscriptions'},
    ]
    
    categories = []
    for data in categories_data:
        category, created = Category.objects.get_or_create(
            name=data['name'],
            defaults={'description': data['description']}
        )
        categories.append(category)
        print(f"  ✓ {category.name}")
    
    return categories

def create_suppliers():
    """Create suppliers"""
    print("Creating suppliers...")
    
    suppliers_data = [
        {
            'name': 'TechSupply Co.',
            'contact_person': 'John Smith',
            'email': 'john@techsupply.com',
            'phone': '+1-555-1001',
            'address': '100 Tech Ave, Silicon Valley, CA 94025'
        },
        {
            'name': 'Office Plus',
            'contact_person': 'Sarah Johnson',
            'email': 'sarah@officeplus.com',
            'phone': '+1-555-1002',
            'address': '200 Business St, New York, NY 10001'
        },
        {
            'name': 'Hardware Hub',
            'contact_person': 'Mike Davis',
            'email': 'mike@hardwarehub.com',
            'phone': '+1-555-1003',
            'address': '300 Industry Rd, Detroit, MI 48201'
        },
    ]
    
    suppliers = []
    for data in suppliers_data:
        supplier, created = Supplier.objects.get_or_create(
            name=data['name'],
            defaults={
                'contact_person': data['contact_person'],
                'email': data['email'],
                'phone': data['phone'],
                'address': data['address']
            }
        )
        suppliers.append(supplier)
        print(f"  ✓ {supplier.name}")
    
    return suppliers

def create_stock_items(categories, suppliers):
    """Create stock items"""
    print("Creating stock items...")
    
    items_data = [
        # Electronics
        {'name': 'Laptop Dell XPS 15', 'sku': 'ELEC-001', 'category': 0, 'supplier': 0, 'quantity': 25, 'unit_price': 1299.99, 'reorder_level': 10},
        {'name': 'Wireless Mouse Logitech', 'sku': 'ELEC-002', 'category': 0, 'supplier': 0, 'quantity': 150, 'unit_price': 29.99, 'reorder_level': 50},
        {'name': 'USB-C Hub Anker', 'sku': 'ELEC-003', 'category': 0, 'supplier': 0, 'quantity': 75, 'unit_price': 49.99, 'reorder_level': 30},
        
        # Furniture
        {'name': 'Office Chair Ergonomic', 'sku': 'FURN-001', 'category': 1, 'supplier': 1, 'quantity': 45, 'unit_price': 299.99, 'reorder_level': 15},
        {'name': 'Standing Desk Adjustable', 'sku': 'FURN-002', 'category': 1, 'supplier': 1, 'quantity': 20, 'unit_price': 549.99, 'reorder_level': 10},
        {'name': 'Monitor Stand Dual', 'sku': 'FURN-003', 'category': 1, 'supplier': 1, 'quantity': 60, 'unit_price': 79.99, 'reorder_level': 20},
        
        # Stationery
        {'name': 'Paper A4 Ream (500 sheets)', 'sku': 'STAT-001', 'category': 2, 'supplier': 1, 'quantity': 200, 'unit_price': 6.99, 'reorder_level': 100},
        {'name': 'Pen Set Blue (10 pack)', 'sku': 'STAT-002', 'category': 2, 'supplier': 1, 'quantity': 8, 'unit_price': 4.99, 'reorder_level': 20},  # Low stock
        {'name': 'Notebook A5 Ruled', 'sku': 'STAT-003', 'category': 2, 'supplier': 1, 'quantity': 120, 'unit_price': 3.99, 'reorder_level': 50},
        
        # Hardware
        {'name': 'Screwdriver Set Professional', 'sku': 'HARD-001', 'category': 3, 'supplier': 2, 'quantity': 35, 'unit_price': 49.99, 'reorder_level': 15},
        {'name': 'Power Drill Cordless', 'sku': 'HARD-002', 'category': 3, 'supplier': 2, 'quantity': 18, 'unit_price': 129.99, 'reorder_level': 10},
        {'name': 'Measuring Tape 25ft', 'sku': 'HARD-003', 'category': 3, 'supplier': 2, 'quantity': 5, 'unit_price': 12.99, 'reorder_level': 20},  # Low stock
    ]
    
    stocks = []
    for item in items_data:
        stock, created = Stock.objects.get_or_create(
            sku=item['sku'],
            defaults={
                'name': item['name'],
                'category': categories[item['category']],
                'supplier': suppliers[item['supplier']],
                'quantity': item['quantity'],
                'unit_price': Decimal(str(item['unit_price'])),
                'reorder_level': item['reorder_level']
            }
        )
        stocks.append(stock)
        status = "⚠ Low stock" if stock.quantity <= stock.reorder_level else ""
        print(f"  ✓ {stock.sku} - {stock.name} ({stock.quantity} units) {status}")
    
    return stocks

def create_sample_transactions(admin, stocks, suppliers):
    """Create sample purchase and sale transactions"""
    print("Creating sample transactions...")
    
    # Create 3 purchases
    for i in range(3):
        purchase = Purchase.objects.create(
            supplier=random.choice(suppliers),
            date=date.today() - timedelta(days=random.randint(1, 30)),
            total_amount=Decimal('0.00'),
            created_by=admin
        )
        
        # Add 2-3 items to each purchase
        total = Decimal('0.00')
        for j in range(random.randint(2, 3)):
            stock = random.choice(stocks)
            quantity = random.randint(10, 50)
            PurchaseItem.objects.create(
                purchase=purchase,
                stock=stock,
                quantity=quantity,
                unit_price=stock.unit_price
            )
            total += stock.unit_price * quantity
            
            # Update stock quantity
            prev_qty = stock.quantity
            stock.quantity += quantity
            stock.save()
            
            # Create stock history
            StockHistory.objects.create(
                stock=stock,
                direction='IN',
                quantity=quantity,
                previous_quantity=prev_qty,
                new_quantity=stock.quantity,
                note=f'Purchase from {purchase.supplier.name} (PO-{purchase.id})',
                created_by=admin
            )
        
        purchase.total_amount = total
        purchase.save()
        print(f"  ✓ Purchase #{purchase.id} - ${total}")
    
    # Create 2 sales
    for i in range(2):
        sale = Sale.objects.create(
            customer_name=random.choice(['ABC Corp', 'XYZ Ltd', 'Tech Solutions Inc']),
            date=date.today() - timedelta(days=random.randint(1, 15)),
            total_amount=Decimal('0.00'),
            discount=Decimal('0.00'),
            created_by=admin
        )
        
        # Add 1-2 items to each sale
        total = Decimal('0.00')
        for j in range(random.randint(1, 2)):
            stock = random.choice([s for s in stocks if s.quantity > 10])  # Only stocks with sufficient quantity
            quantity = random.randint(1, 5)
            SaleItem.objects.create(
                sale=sale,
                stock=stock,
                quantity=quantity,
                unit_price=stock.unit_price
            )
            total += stock.unit_price * quantity
            
            # Update stock quantity
            prev_qty = stock.quantity
            stock.quantity -= quantity
            stock.save()
            
            # Create stock history
            StockHistory.objects.create(
                stock=stock,
                direction='OUT',
                quantity=quantity,
                previous_quantity=prev_qty,
                new_quantity=stock.quantity,
                note=f'Sale to {sale.customer_name} (SO-{sale.id})',
                created_by=admin
            )
        
        sale.total_amount = total
        sale.save()
        print(f"  ✓ Sale #{sale.id} - ${total}")

def main():
    print("=" * 50)
    print("Inventory Management System - Demo Data Setup")
    print("=" * 50)
    print()
    
    # Clear existing data
    print("Clearing existing data...")
    SaleItem.objects.all().delete()
    Sale.objects.all().delete()
    PurchaseItem.objects.all().delete()
    Purchase.objects.all().delete()
    StockHistory.objects.all().delete()
    Stock.objects.all().delete()
    Supplier.objects.all().delete()
    Category.objects.all().delete()
    
    if HAS_HOMEPAGE_MODELS:
        try:
            ActivityLog.objects.all().delete()
            UserProfile.objects.all().delete()
        except Exception as e:
            print(f"  Note: Could not clear homepage models: {e}")
    
    User.objects.filter(username='admin@example.com').delete()
    print()
    
    # Create data
    admin = create_admin_user()
    print()
    
    categories = create_categories()
    print()
    
    suppliers = create_suppliers()
    print()
    
    stocks = create_stock_items(categories, suppliers)
    print()
    
    create_sample_transactions(admin, stocks, suppliers)
    print()
    
    print("=" * 50)
    print("✓ Demo data created successfully!")
    print("=" * 50)
    print()
    print("Login Credentials:")
    print("-" * 30)
    print("Email:    admin@example.com")
    print("Password: admin123")
    print()
    print("You can also register a new account!")
    print()

if __name__ == '__main__':
    main()
