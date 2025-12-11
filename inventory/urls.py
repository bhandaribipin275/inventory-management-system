from django.urls import path
from django.conf.urls import url
from . import views

app_name = 'inventory'

urlpatterns = [
    path('', views.inventory_list, name='inventory_list'),
    path('stock/<int:pk>/', views.stock_change, name='stock_change'),
    path('list', views.StockListView.as_view(), name='inventory'),
    path('new', views.StockCreateView.as_view(), name='new-stock'),
    path('stock/<pk>/edit', views.StockUpdateView.as_view(), name='edit-stock'),
    path('stock/<pk>/delete', views.StockDeleteView.as_view(), name='delete-stock'),
]