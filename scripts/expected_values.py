from inventory.models import Item
from decimal import Decimal

all_items = list(Item.objects.all().order_by('name'))
low_items = [i for i in all_items if i.quantity <= 5]

total = Decimal('0.00')
for i in all_items:
    qty_dec = Decimal(str(i.quantity))
    price_dec = Decimal(str(i.price))
    total += qty_dec * price_dec

print('=== Dashboard Verification ===\n')
print(f'Total items in database: {len(all_items)}')
print(f'Items with low stock (≤5): {len(low_items)}')
print(f'Expected total inventory value: ₹{total:.2f}\n')

print('Low stock items:')
for item in low_items:
    print(f'  - {item.name:15} qty={item.quantity}, price={item.price}, category={item.category}')

print(f'\nExpected total: ₹{float(total):.2f}')
print(f'Item breakdown:')
for item in all_items:
    qty_dec = Decimal(str(item.quantity))
    price_dec = Decimal(str(item.price))
    item_total = qty_dec * price_dec
    print(f'  {item.name:15} {item.quantity:2} × {float(item.price):6.2f} = {float(item_total):8.2f}')
