from django.contrib.auth.models import User
from django.test import Client
from inventory.models import Item
from decimal import Decimal

# Log in as admin
user = User.objects.get(username='admin')
client = Client()
client.force_login(user)

# Request dashboard (no follow, so we can get context)
resp = client.get('/', HTTP_HOST='127.0.0.1', follow=False)
print('Dashboard status:', resp.status_code)

# Check context
if resp.context:
    # Check total_value in context
    if 'total_value' in resp.context:
        total_value = resp.context['total_value']
        print(f'\n✓ Total inventory value: ₹{total_value}')
        
        # Manually verify the calculation
        items = Item.objects.all()
        expected_total = sum((Decimal(i.quantity) * i.price for i in items), Decimal('0.00'))
        print(f'  Expected (calculated): ₹{expected_total}')
        if abs(float(total_value) - float(expected_total)) < 0.01:
            print(f'  ✓ Value calculation is correct')
        else:
            print(f'  ✗ Mismatch!')
    else:
        print('✗ total_value not in context')

    # Check low_stock_items
    if 'low_stock_items' in resp.context:
        low_items = resp.context['low_stock_items']
        print(f'\n✓ Low stock items (≤5): {len(low_items)} found')
        for it in low_items:
            print(f'    - {it.name} (qty={it.quantity})')
        
        # Verify count matches expected
        expected_low = Item.objects.filter(quantity__lte=5).count()
        if len(low_items) == expected_low:
            print(f'  ✓ Count matches expected: {expected_low}')
        else:
            print(f'  ✗ Expected {expected_low}, got {len(low_items)}')
    else:
        print('✗ low_stock_items not in context')

    # Check low_ids
    if 'low_ids' in resp.context:
        low_ids = resp.context['low_ids']
        print(f'\n✓ Low stock IDs set: {len(low_ids)} items')
    else:
        print('✗ low_ids not in context')

    # Check low_threshold
    if 'low_threshold' in resp.context:
        threshold = resp.context['low_threshold']
        print(f'\n✓ Low threshold: {threshold}')
    else:
        print('✗ low_threshold not in context')

else:
    print('✗ No context available')

# Parse HTML to verify rendering
content = resp.content.decode('utf-8')

print('\n--- HTML Verification ---')
if 'low-row' in content:
    print('✓ Low-row CSS class found in HTML')
else:
    print('✗ Low-row CSS class NOT found in HTML')

for header in ['<th>Category</th>', '<th>Brand</th>', '<th>Expiry</th>']:
    if header in content:
        print(f'✓ {header} found')
    else:
        print(f'✗ {header} NOT found')

# Sample low-stock item names should appear in HTML
items_with_qty_low = Item.objects.filter(quantity__lte=5).values_list('name', flat=True)
found_count = 0
for name in items_with_qty_low:
    if name in content:
        found_count += 1
print(f'✓ {found_count}/{items_with_qty_low.count()} low-stock items found in table HTML')
