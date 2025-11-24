from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

from .models import Stock
from .forms import StockForm


# ============================
#   STOCK LIST WITH SEARCH
# ============================
class StockListView(ListView):
    model = Stock
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = "inventory/inventory.html"
    context_object_name = "stocks"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get("q")

        if query:
            queryset = queryset.filter(
                Q(name__icontains=query)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


# ============================
#   CREATE STOCK
# ============================
class StockCreateView(SuccessMessageMixin, CreateView):
    model = Stock
    form_class = StockForm
    template_name = "inventory/add_stock.html"
    success_url = reverse_lazy("inventory")
    success_message = "Stock has been created successfully."


# ============================
#   UPDATE STOCK
# ============================
class StockUpdateView(SuccessMessageMixin, UpdateView):
    model = Stock
    form_class = StockForm
    template_name = "inventory/edit_stock.html"
    success_url = reverse_lazy("inventory")
    success_message = "Stock has been updated successfully."

    def get_object(self, queryset=None):
        return get_object_or_404(Stock, pk=self.kwargs["pk"], is_deleted=False)


# ============================
#   DELETE STOCK (SOFT DELETE)
# ============================
class StockDeleteView(DeleteView):
    model = Stock
    template_name = "inventory/delete_stock.html"
    success_url = reverse_lazy("inventory")

    def get_object(self, queryset=None):
        return get_object_or_404(Stock, pk=self.kwargs["pk"], is_deleted=False)

    def delete(self, request, *args, **kwargs):
        stock = self.get_object()
        stock.is_deleted = True
        stock.save()
        messages.success(request, "Stock deleted successfully.")
        return super().delete(request, *args, **kwargs)