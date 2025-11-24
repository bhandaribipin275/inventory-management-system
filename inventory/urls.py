from django.urls import path

from .views import (
    StockListView,
    StockCreateView,
    StockUpdateView,
    StockDeleteView,
)

urlpatterns = [
    path("", StockListView.as_view(), name="inventory"),
    path("add/", StockCreateView.as_view(), name="add_stock"),
    path("<int:pk>/edit/", StockUpdateView.as_view(), name="edit_stock"),
    path("<int:pk>/delete/", StockDeleteView.as_view(), name="delete_stock"),
]