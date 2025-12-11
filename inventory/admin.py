from django.contrib import admin
from .models import Item, Stock

@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'sku', 'quantity', 'price', 'category', 'brand', 'expiry_date')
    list_filter = ('category', 'brand')
    search_fields = ('name', 'sku', 'category', 'brand')
    ordering = ('name',)

@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'is_deleted')
    list_filter = ('is_deleted',)
    search_fields = ('name',)
