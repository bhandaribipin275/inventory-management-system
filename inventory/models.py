from decimal import Decimal
from django.db import models
from django.utils import timezone

class Stock(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30, unique=True, verbose_name='Name')
    quantity = models.IntegerField(default=1)
    is_deleted = models.BooleanField(default=False)

    def __str__(self):
	    return self.name

class StockHistory(models.Model):
    IN = 'IN'
    OUT = 'OUT'
    TYPE_CHOICES = [
        (IN, 'Stock In'),
        (OUT, 'Stock Out'),
    ]

    stock = models.ForeignKey(Stock, on_delete=models.CASCADE, related_name='stock_history')
    change = models.IntegerField()
    type = models.CharField(max_length=3, choices=TYPE_CHOICES)
    timestamp = models.DateTimeField(default=timezone.now)
    note = models.CharField(max_length=255, blank=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.timestamp} - {self.stock.name} - {self.type} {self.change}"
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=100, unique=True)
    quantity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # New metadata fields
    expiry_date = models.DateField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True)
    brand = models.CharField(max_length=100, blank=True)

    def is_low_stock(self, threshold=5):
        """
        Returns True if quantity is less than or equal to threshold.
        Default threshold is 5 but callers can pass a different value.
        """
        return self.quantity <= threshold

    def total_value(self):
        """
        Returns Decimal total value for this item (quantity * price).
        """
        return Decimal(self.quantity) * self.price

    def __str__(self):
        # Friendly representation without exposing sensitive data
        return self.name or self.sku
