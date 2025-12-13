#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from inventory.models import Stock
from transactions.models import Supplier, PurchaseBill, PurchaseItem, SaleBill, SaleItem
from decimal import Decimal
import random
from datetime import datetime

# Check what stocks exist
existing_stocks = Stock.objects.all()
print(f"Existing stocks in database: {existing_stocks.count()}")
for stock in existing_stocks:
    print(f"  - {stock.name}: {stock.quantity} units")

# Check existing suppliers
existing_suppliers = Supplier.objects.all()
print(f"\nExisting suppliers: {existing_suppliers.count()}")
for supplier in existing_suppliers:
    print(f"  - {supplier.name}")

if existing_suppliers.count() == 0:
    # Create test suppliers if none exist
    supplier1 = Supplier.objects.create(
        name='Tech Supplies Ltd', 
        email='info@techsupplies.com', 
        phone='1234567890',
        address='123 Tech Street, Tech City',
        gstin='18AABCT1234B1Z5'
    )
    print(f"\n✓ Created supplier: {supplier1.name}")
else:
    supplier1 = existing_suppliers.first()

# Create a sample purchase bill if we have both stocks and suppliers
if existing_stocks.count() > 0 and supplier1:
    try:
        purchase_bill = PurchaseBill.objects.create(
            supplier=supplier1,
            time=datetime.now()
        )
        
        # Add purchase items
        for stock in existing_stocks[:2]:  # Add first 2 stocks to purchase
            PurchaseItem.objects.create(
                billno=purchase_bill,
                stock=stock,
                quantity=10,
                perprice=Decimal('100.00')
            )
        
        print(f"\n✓ Created test purchase bill #{purchase_bill.billno}")
        print(f"  - Supplier: {supplier1.name}")
        print(f"  - Items: 2")
        
    except Exception as e:
        print(f"Note: {str(e)}")

print("\n✓ Test data setup complete!")
