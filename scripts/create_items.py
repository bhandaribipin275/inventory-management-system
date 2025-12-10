from inventory.models import Item
from datetime import date, timedelta

items_data = [
    {'name': 'Widget A', 'sku': 'SKU001', 'quantity': 3, 'price': 10.50, 'category': 'Widgets', 'brand': 'BrandX', 'expiry_date': date.today() + timedelta(days=30)},
    {'name': 'Widget B', 'sku': 'SKU002', 'quantity': 5, 'price': 15.00, 'category': 'Widgets', 'brand': 'BrandY', 'expiry_date': date.today() + timedelta(days=60)},
    {'name': 'Gadget A', 'sku': 'SKU003', 'quantity': 12, 'price': 25.99, 'category': 'Gadgets', 'brand': 'BrandZ', 'expiry_date': date.today() + timedelta(days=90)},
    {'name': 'Gadget B', 'sku': 'SKU004', 'quantity': 2, 'price': 30.00, 'category': 'Gadgets', 'brand': 'BrandX', 'expiry_date': date.today() + timedelta(days=45)},
    {'name': 'Tool A', 'sku': 'SKU005', 'quantity': 8, 'price': 45.00, 'category': 'Tools', 'brand': 'BrandA', 'expiry_date': None},
    {'name': 'Tool B', 'sku': 'SKU006', 'quantity': 1, 'price': 55.00, 'category': 'Tools', 'brand': 'BrandB', 'expiry_date': date.today() + timedelta(days=120)},
    {'name': 'Supply A', 'sku': 'SKU007', 'quantity': 20, 'price': 5.50, 'category': 'Supplies', 'brand': 'BrandC', 'expiry_date': date.today() + timedelta(days=180)},
    {'name': 'Supply B', 'sku': 'SKU008', 'quantity': 4, 'price': 7.99, 'category': 'Supplies', 'brand': 'BrandD', 'expiry_date': date.today() + timedelta(days=75)},
]

for data in items_data:
    item, created = Item.objects.get_or_create(
        sku=data['sku'],
        defaults={
            'name': data['name'],
            'quantity': data['quantity'],
            'price': data['price'],
            'category': data['category'],
            'brand': data['brand'],
            'expiry_date': data['expiry_date'],
        }
    )
    status = 'created' if created else 'exists'
    print(f"{item.name:15} (qty={item.quantity:2}, price={item.price:6.2f}, category={item.category:10}) - {status}")

print(f'\nTotal items: {Item.objects.count()}')
