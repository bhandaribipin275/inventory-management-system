from django.contrib.auth.models import User
from django.test import Client
from inventory.models import Item
from decimal import Decimal

# Log in as admin
user = User.objects.get(username='admin')
client = Client()
client.force_login(user)

# Request dashboard
resp = client.get('/', HTTP_HOST='127.0.0.1')
print('Dashboard status:', resp.status_code)

# Parse response
content = resp.content.decode('utf-8')

# Check context (may be empty if redirect happens)
if resp.context:
    # Check total_value in context
    if 'total_value' in resp.context:
        total_value = resp.context['total_value']
        print(f'Total inventory value: ₹{total_value}')
    else:
        print('ERROR: total_value not in context')

    # Check low_stock_items
    if 'low_stock_items' in resp.context:
        low_items = resp.context['low_stock_items']
        print(f'\nLow stock items (≤5): {len(low_items)} found')
        for it in low_items:
            print(f'  - {it.name} (qty={it.quantity})')
    else:
        print('ERROR: low_stock_items not in context')

    # Check low_ids
    if 'low_ids' in resp.context:
        low_ids = resp.context['low_ids']
        print(f'Low stock IDs: {low_ids}')
    else:
        print('ERROR: low_ids not in context')
else:
    print('No context (likely redirected)')

# Check HTML for table rows with low-row class
if 'low-row' in content:
    print('\n✓ Low-row CSS class found in HTML (rows should be highlighted)')
else:
    print('\n✗ Low-row CSS class NOT found in HTML')

# Check HTML for Category, Brand, Expiry headers
for header in ['<th>Category</th>', '<th>Brand</th>', '<th>Expiry</th>']:
    if header in content:
        print(f'✓ {header} found in table header')
    else:
        print(f'✗ {header} NOT found in table header')

# Check for total_value in HTML
if '₹' in content or 'total_value' in content or 'Total inventory' in content:
    print('✓ Total inventory value section found in HTML')
else:
    print('✗ Total inventory value section NOT found in HTML')

# Verify at least one low-qty item row is in HTML
items_with_qty_low = Item.objects.filter(quantity__lte=5)
for it in items_with_qty_low:
    if it.name in content:
        print(f'✓ Item "{it.name}" (qty={it.quantity}) found in table')
        break

