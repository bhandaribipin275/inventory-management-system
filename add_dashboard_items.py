#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from inventory.models import Item
from decimal import Decimal

# Create test items for the dashboard
items_data = [
    {'name': 'Laptop', 'sku': 'LAP-001', 'quantity': 5, 'price': Decimal('50000.00'), 'category': 'Electronics', 'brand': 'Dell'},
    {'name': 'Mouse', 'sku': 'MOU-001', 'quantity': 150, 'price': Decimal('500.00'), 'category': 'Accessories', 'brand': 'Logitech'},
    {'name': 'Keyboard', 'sku': 'KEY-001', 'quantity': 3, 'price': Decimal('2000.00'), 'category': 'Accessories', 'brand': 'Corsair'},
    {'name': 'Monitor', 'sku': 'MON-001', 'quantity': 12, 'price': Decimal('15000.00'), 'category': 'Electronics', 'brand': 'LG'},
    {'name': 'USB Cable', 'sku': 'USB-001', 'quantity': 2, 'price': Decimal('300.00'), 'category': 'Accessories', 'brand': 'Generic'},
    {'name': 'HDMI Cable', 'sku': 'HDM-001', 'quantity': 25, 'price': Decimal('400.00'), 'category': 'Accessories', 'brand': 'Generic'},
]

print("Creating test items for the dashboard...")
created_count = 0

for item_data in items_data:
    # Check if item already exists
    if not Item.objects.filter(sku=item_data['sku']).exists():
        Item.objects.create(**item_data)
        created_count += 1
        print(f"✓ Created: {item_data['name']} ({item_data['quantity']} units @ ₹{item_data['price']})")
    else:
        print(f"⊘ Already exists: {item_data['name']}")

print(f"\n✓ Total items created: {created_count}")
print(f"✓ Total items in database: {Item.objects.count()}")

# Calculate and display stats
total_value = sum((item.total_value() for item in Item.objects.all()), Decimal('0.00'))
print(f"\n✓ Total inventory value: ₹{total_value:,.2f}")

# Show low stock items
low_threshold = 5
low_stock = [item for item in Item.objects.all() if item.is_low_stock(low_threshold)]
if low_stock:
    print(f"\n⚠ Low stock items (≤ {low_threshold} units):")
    for item in low_stock:
        print(f"  - {item.name}: {item.quantity} units")
else:
    print(f"\n✓ No low stock items")
