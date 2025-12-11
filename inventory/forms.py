from django import forms
from .models import Stock, Item

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['name', 'quantity']

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'sku', 'quantity', 'price', 'category', 'brand', 'expiry_date']
        widgets = {
            'expiry_date': forms.DateInput(attrs={'type': 'date'}),
        }
