from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from inventory.models import Stock, StockHistory
from datetime import datetime
from django.utils import timezone


class StockModelTest(TestCase):
    """Test the Stock model"""
    
    def setUp(self):
        self.stock = Stock.objects.create(name="Test Stock", quantity=10)
    
    def test_stock_creation(self):
        """Test that a stock can be created"""
        self.assertEqual(self.stock.name, "Test Stock")
        self.assertEqual(self.stock.quantity, 10)
    
    def test_stock_str_representation(self):
        """Test the string representation of a stock"""
        self.assertEqual(str(self.stock), "Test Stock")


class StockHistoryModelTest(TestCase):
    """Test the StockHistory model"""
    
    def setUp(self):
        self.stock = Stock.objects.create(name="Test Stock", quantity=10)
    
    def test_stock_history_creation_stock_in(self):
        """Test creating a stock in history record"""
        history = StockHistory.objects.create(
            stock=self.stock,
            change=5,
            type=StockHistory.IN,
            note="Initial stock"
        )
        self.assertEqual(history.change, 5)
        self.assertEqual(history.type, StockHistory.IN)
        self.assertEqual(history.stock.name, "Test Stock")
        self.assertEqual(history.note, "Initial stock")
    
    def test_stock_history_creation_stock_out(self):
        """Test creating a stock out history record"""
        history = StockHistory.objects.create(
            stock=self.stock,
            change=3,
            type=StockHistory.OUT,
            note="Sold to customer"
        )
        self.assertEqual(history.change, 3)
        self.assertEqual(history.type, StockHistory.OUT)
    
    def test_stock_history_ordering(self):
        """Test that stock history is ordered by timestamp descending"""
        history1 = StockHistory.objects.create(
            stock=self.stock,
            change=5,
            type=StockHistory.IN
        )
        history2 = StockHistory.objects.create(
            stock=self.stock,
            change=3,
            type=StockHistory.OUT
        )
        histories = StockHistory.objects.all()
        # Most recent should be first
        self.assertEqual(histories[0].id, history2.id)
        self.assertEqual(histories[1].id, history1.id)
    
    def test_stock_history_str_representation(self):
        """Test the string representation of stock history"""
        history = StockHistory.objects.create(
            stock=self.stock,
            change=5,
            type=StockHistory.IN
        )
        str_repr = str(history)
        self.assertIn("Test Stock", str_repr)
        self.assertIn("IN", str_repr)
        self.assertIn("5", str_repr)


class InventoryListViewTest(TestCase):
    """Test the inventory list view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.stock1 = Stock.objects.create(name="Stock A", quantity=10)
        self.stock2 = Stock.objects.create(name="Stock B", quantity=5)
        
        # Create some stock history
        StockHistory.objects.create(
            stock=self.stock1,
            change=10,
            type=StockHistory.IN,
            note="Initial stock"
        )
        StockHistory.objects.create(
            stock=self.stock2,
            change=5,
            type=StockHistory.IN,
            note="Initial stock"
        )
    
    def test_inventory_list_view_requires_login(self):
        """Test that inventory list view requires authentication"""
        response = self.client.get(reverse('inventory:inventory_list'))
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_inventory_list_view_authenticated(self):
        """Test inventory list view for authenticated user"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory:inventory_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/inventory_list.html')
    
    def test_inventory_list_contains_items(self):
        """Test that inventory list view displays items"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory:inventory_list'))
        self.assertContains(response, "Stock A")
        self.assertContains(response, "Stock B")
    
    def test_inventory_list_contains_history(self):
        """Test that inventory list view displays stock history"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory:inventory_list'))
        self.assertContains(response, "Initial stock")
    
    def test_inventory_list_context(self):
        """Test that the context contains items and history"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('inventory:inventory_list'))
        self.assertIn('items', response.context)
        self.assertIn('history', response.context)
        self.assertEqual(len(response.context['items']), 2)


class StockChangeViewTest(TestCase):
    """Test the stock change view"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.stock = Stock.objects.create(name="Test Stock", quantity=10)
    
    def test_stock_change_view_get(self):
        """Test GET request to stock change view"""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(
            reverse('inventory:stock_change', args=[self.stock.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'inventory/stock_change.html')
        self.assertIn('item', response.context)
    
    def test_stock_change_view_stock_in(self):
        """Test stock in operation"""
        self.client.login(username='testuser', password='testpass123')
        initial_qty = self.stock.quantity
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': 5,
                'type': StockHistory.IN,
                'note': 'Restocking'
            }
        )
        
        # Verify item quantity increased
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, initial_qty + 5)
        
        # Verify history record created
        history = StockHistory.objects.filter(stock=self.stock).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.change, 5)
        self.assertEqual(history.type, StockHistory.IN)
        self.assertEqual(history.note, 'Restocking')
    
    def test_stock_change_view_stock_out(self):
        """Test stock out operation"""
        self.client.login(username='testuser', password='testpass123')
        initial_qty = self.stock.quantity
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': 3,
                'type': StockHistory.OUT,
                'note': 'Sold'
            }
        )
        
        # Verify item quantity decreased
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, initial_qty - 3)
        
        # Verify history record created
        history = StockHistory.objects.filter(stock=self.stock).first()
        self.assertIsNotNone(history)
        self.assertEqual(history.change, 3)
        self.assertEqual(history.type, StockHistory.OUT)
    
    def test_stock_change_view_stock_out_no_negative(self):
        """Test that stock out doesn't go below zero"""
        self.client.login(username='testuser', password='testpass123')
        self.stock.quantity = 2
        self.stock.save()
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': 10,
                'type': StockHistory.OUT,
                'note': 'Test'
            }
        )
        
        # Verify quantity is 0, not negative
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, 0)
    
    def test_stock_change_view_invalid_change(self):
        """Test that invalid change value is rejected"""
        self.client.login(username='testuser', password='testpass123')
        initial_qty = self.stock.quantity
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': -5,  # Invalid negative value
                'type': StockHistory.IN,
                'note': 'Test'
            }
        )
        
        # Verify item quantity unchanged
        self.stock.refresh_from_db()
        self.assertEqual(self.stock.quantity, initial_qty)
        
        # Verify error message in response
        self.assertContains(response, 'Please enter a positive integer')
    
    def test_stock_change_view_zero_change_rejected(self):
        """Test that zero change value is rejected"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': 0,
                'type': StockHistory.IN,
                'note': 'Test'
            }
        )
        
        self.assertContains(response, 'Please enter a positive integer')
    
    def test_stock_change_view_non_numeric_change(self):
        """Test that non-numeric change value is handled"""
        self.client.login(username='testuser', password='testpass123')
        initial_qty = self.stock.quantity
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': 'abc',  # Non-numeric
                'type': StockHistory.IN,
                'note': 'Test'
            }
        )
        
        # Should show error
        self.assertContains(response, 'Please enter a positive integer')
    
    def test_stock_change_view_redirect_on_success(self):
        """Test that successful stock change redirects to inventory list"""
        self.client.login(username='testuser', password='testpass123')
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[self.stock.pk]),
            {
                'change': 5,
                'type': StockHistory.IN,
                'note': 'Test'
            }
        )
        
        # Should redirect
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse('inventory:inventory_list'), response.url)



class StockHistoryIntegrationTest(TestCase):
    """Integration tests for stock history feature"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
    
    def test_multiple_stock_operations(self):
        """Test multiple stock operations in sequence"""
        self.client.login(username='testuser', password='testpass123')
        stock = Stock.objects.create(name="Test Stock", quantity=0)
        
        # Stock in 10
        self.client.post(
            reverse('inventory:stock_change', args=[stock.pk]),
            {'change': 10, 'type': StockHistory.IN, 'note': 'Received'}
        )
        
        # Stock in 5
        self.client.post(
            reverse('inventory:stock_change', args=[stock.pk]),
            {'change': 5, 'type': StockHistory.IN, 'note': 'Received'}
        )
        
        # Stock out 8
        self.client.post(
            reverse('inventory:stock_change', args=[stock.pk]),
            {'change': 8, 'type': StockHistory.OUT, 'note': 'Sold'}
        )
        
        # Verify final quantity
        stock.refresh_from_db()
        self.assertEqual(stock.quantity, 7)
        
        # Verify history records
        histories = StockHistory.objects.filter(stock=stock).order_by('-timestamp')
        self.assertEqual(histories.count(), 3)
    
    def test_stock_history_with_notes(self):
        """Test that notes are properly saved and displayed"""
        self.client.login(username='testuser', password='testpass123')
        stock = Stock.objects.create(name="Test Stock", quantity=10)
        
        response = self.client.post(
            reverse('inventory:stock_change', args=[stock.pk]),
            {
                'change': 5,
                'type': StockHistory.IN,
                'note': 'Supplier: ABC Company, Invoice: INV-001'
            }
        )
        
        history = StockHistory.objects.filter(stock=stock).first()
        self.assertEqual(history.note, 'Supplier: ABC Company, Invoice: INV-001')
    
    def test_inventory_list_shows_latest_history(self):
        """Test that inventory list shows latest 20 history entries"""
        self.client.login(username='testuser', password='testpass123')
        stock = Stock.objects.create(name="Test Stock", quantity=0)
        
        # Create 25 history records
        for i in range(25):
            StockHistory.objects.create(
                stock=stock,
                change=1,
                type=StockHistory.IN,
                note=f"Note {i}"
            )
        
        response = self.client.get(reverse('inventory:inventory_list'))
        
        # Should only show 20 latest
        self.assertEqual(len(response.context['history']), 20)

