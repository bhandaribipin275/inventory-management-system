from django.contrib.auth.models import User
from django.test import Client

# Log in as admin
user = User.objects.get(username='admin')
client = Client()
client.force_login(user)

# Request dashboard
resp = client.get('/', HTTP_HOST='127.0.0.1', follow=False)
print('Dashboard status:', resp.status_code)
print('Content-Type:', resp.get('Content-Type'))
print('Location:', resp.get('Location', 'N/A'))
print()
print('First 500 chars of response:')
print(resp.content.decode('utf-8')[:500])
