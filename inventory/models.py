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