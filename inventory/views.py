from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.generic import (
    View,
    CreateView, 
    UpdateView
)
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.utils import timezone
from .models import Stock, StockHistory
from .forms import StockForm
from django_filters.views import FilterView
from .filters import StockFilter
from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib import messages
from django.db.models import Q

from .models import Stock, Item
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
            queryset = queryset.filter(Q(name__icontains=query))
        return queryset

class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory/list'                                                     # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["q"] = self.request.GET.get("q", "")
        return context


class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory/list'                                                     # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"                             # displays message when form is submitted
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
        messages.success(request, self.success_message)
        return redirect('inventory')


def inventory_list(request):
    """
    List stocks and show a short stock history preview.
    """
    stocks = Stock.objects.filter(is_deleted=False).order_by('name')
    # show latest 20 history entries
    history = StockHistory.objects.select_related('stock')[:20]
    return render(request, 'inventory/inventory_list.html', {
        'items': stocks,
        'history': history,
    })

@require_http_methods(["GET", "POST"])
def stock_change(request, pk):
    """
    Form to record stock in or stock out for a single stock item.
    On POST, create StockHistory and update Stock.quantity.
    """
    stock = get_object_or_404(Stock, pk=pk)

    if request.method == 'POST':
        # Expect form fields: change (int), type (IN/OUT), note (optional)
        try:
            change = int(request.POST.get('change', '0'))
        except ValueError:
            change = 0

        typ = request.POST.get('type', 'IN')
        note = request.POST.get('note', '').strip()

        if change <= 0:
            # invalid change, re-render with error
            return render(request, 'inventory/stock_change.html', {
                'item': stock,
                'error': 'Please enter a positive integer for change.',
            })

        # Apply change
        if typ == StockHistory.IN:
            stock.quantity += change
        else:
            # Stock out: ensure we don't go negative (you can change this behavior)
            stock.quantity = max(0, stock.quantity - change)

        stock.save()

        StockHistory.objects.create(
            stock=stock,
            change=change,
            type=typ,
            timestamp=timezone.now(),
            note=note
        )

        return redirect(reverse('inventory:inventory_list'))

    # GET
    return render(request, 'inventory/stock_change.html', {'item': stock})
        stock.save()
        messages.success(request, "Stock deleted successfully.")
        return super().delete(request, *args, **kwargs)


# ============================
#   DASHBOARD
# ============================
def dashboard(request):
    """
    Dashboard view:
    - highlights low stock items (threshold configurable)
    - computes total inventory value (Decimal-safe)
    - passes low_ids set for template conditional checks
    """
    low_threshold = 5  # change this value to adjust what counts as low stock
    items = Item.objects.all().order_by('name')
    # compute low stock items and a set of their ids for fast template checks
    low_stock_items = [i for i in items if i.is_low_stock(low_threshold)]
    low_ids = {i.id for i in low_stock_items}
    # sum total value using Decimal start to avoid mixing types
    total_value = sum((i.total_value() for i in items), Decimal('0.00'))

    context = {
        'items': items,
        'low_stock_items': low_stock_items,
        'low_threshold': low_threshold,
        'low_ids': low_ids,
        'total_value': total_value,
    }
    return render(request, 'dashboard.html', context)
