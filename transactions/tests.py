from django.test import TestCase, Client
from django.contrib.auth.models import User
from transactions.models import (
    Supplier, 
    PurchaseBill, 
    PurchaseItem, 
    PurchaseBillDetails,
    SaleBill,
    SaleItem,
    SaleBillDetails
)
from inventory.models import Stock


class PurchaseFlowTestCase(TestCase):
    """Test purchase bill creation and stock updates."""
    
    def setUp(self):
        """Create test user, supplier, and stock item."""
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass',
            email='test@example.com'
        )
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            phone='9999999999',
            address='123 Test St',
            email='supplier@example.com',
            gstin='TESTGSTIN12345'
        )
        self.stock = Stock.objects.create(
            name='TestStock1',
            quantity=100
        )
        self.client = Client()
        self.client.login(username='testuser', password='testpass')
    
    def test_purchase_bill_creation(self):
        """Test that a purchase bill is created with correct items and details."""
        post_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-stock': str(self.stock.pk),
            'form-0-quantity': '5',
            'form-0-perprice': '50',
        }
        
        url = f'/transactions/purchases/new/{self.supplier.pk}'
        response = self.client.post(url, post_data, follow=True, HTTP_HOST='127.0.0.1')
        
        self.assertEqual(response.status_code, 200)
        
        # Check bill was created
        bills = PurchaseBill.objects.filter(supplier=self.supplier)
        self.assertEqual(bills.count(), 1)
        bill = bills.first()
        
        # Check items
        items = PurchaseItem.objects.filter(billno=bill)
        self.assertEqual(items.count(), 1)
        item = items.first()
        self.assertEqual(item.stock, self.stock)
        self.assertEqual(item.quantity, 5)
        self.assertEqual(item.perprice, 50)
        self.assertEqual(item.totalprice, 250)
        
        # Check details
        details = PurchaseBillDetails.objects.get(billno=bill)
        self.assertEqual(details.total, 250)
    
    def test_purchase_updates_stock_quantity(self):
        """Test that purchasing updates stock quantity correctly."""
        initial_qty = self.stock.quantity
        post_data = {
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-stock': str(self.stock.pk),
            'form-0-quantity': '10',
            'form-0-perprice': '20',
        }
        
        url = f'/transactions/purchases/new/{self.supplier.pk}'
        self.client.post(url, post_data, follow=True, HTTP_HOST='127.0.0.1')
        
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, initial_qty + 10)


class SaleFlowTestCase(TestCase):
    """Test sale bill creation and stock updates."""
    
    def setUp(self):
        """Create test user and stock item."""
        self.user = User.objects.create_user(
            username='testuser2',
            password='testpass',
            email='test2@example.com'
        )
        self.stock = Stock.objects.create(
            name='TestStock2',
            quantity=100
        )
        self.client = Client()
        self.client.login(username='testuser2', password='testpass')
    
    def test_sale_bill_creation(self):
        """Test that a sale bill is created with correct items and details."""
        post_data = {
            'name': 'Test Customer',
            'phone': '8888888888',
            'address': '456 Customer St',
            'email': 'customer@example.com',
            'gstin': 'CUSTGSTIN12345',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-stock': str(self.stock.pk),
            'form-0-quantity': '3',
            'form-0-perprice': '75',
        }
        
        url = '/transactions/sales/new'
        response = self.client.post(url, post_data, follow=True, HTTP_HOST='127.0.0.1')
        
        self.assertEqual(response.status_code, 200)
        
        # Check bill was created
        bills = SaleBill.objects.filter(name='Test Customer')
        self.assertEqual(bills.count(), 1)
        bill = bills.first()
        
        # Check items
        items = SaleItem.objects.filter(billno=bill)
        self.assertEqual(items.count(), 1)
        item = items.first()
        self.assertEqual(item.stock, self.stock)
        self.assertEqual(item.quantity, 3)
        self.assertEqual(item.perprice, 75)
        self.assertEqual(item.totalprice, 225)
        
        # Check details
        details = SaleBillDetails.objects.get(billno=bill)
        self.assertEqual(details.total, 225)
    
    def test_sale_decreases_stock_quantity(self):
        """Test that selling updates stock quantity correctly."""
        initial_qty = self.stock.quantity
        post_data = {
            'name': 'Test Customer',
            'phone': '8888888888',
            'address': '456 Customer St',
            'email': 'customer@example.com',
            'gstin': 'CUSTGSTIN12345',
            'form-TOTAL_FORMS': '1',
            'form-INITIAL_FORMS': '0',
            'form-MIN_NUM_FORMS': '0',
            'form-MAX_NUM_FORMS': '1000',
            'form-0-stock': str(self.stock.pk),
            'form-0-quantity': '7',
            'form-0-perprice': '50',
        }
        
        url = '/transactions/sales/new'
        self.client.post(url, post_data, follow=True, HTTP_HOST='127.0.0.1')
        
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, initial_qty - 7)
