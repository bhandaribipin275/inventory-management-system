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


class StockListView(FilterView):
    filterset_class = StockFilter
    queryset = Stock.objects.filter(is_deleted=False)
    template_name = 'inventory.html'
    paginate_by = 10


class StockCreateView(SuccessMessageMixin, CreateView):                                 # createview class to add new stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory/list'                                                     # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been created successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'New Stock'
        context["savebtn"] = 'Add to Inventory'
        return context       


class StockUpdateView(SuccessMessageMixin, UpdateView):                                 # updateview class to edit stock, mixin used to display message
    model = Stock                                                                       # setting 'Stock' model as model
    form_class = StockForm                                                              # setting 'StockForm' form as form
    template_name = "edit_stock.html"                                                   # 'edit_stock.html' used as the template
    success_url = '/inventory/list'                                                     # redirects to 'inventory' page in the url after submitting the form
    success_message = "Stock has been updated successfully"                             # displays message when form is submitted

    def get_context_data(self, **kwargs):                                               # used to send additional context
        context = super().get_context_data(**kwargs)
        context["title"] = 'Edit Stock'
        context["savebtn"] = 'Update Stock'
        context["delbtn"] = 'Delete Stock'
        return context


class StockDeleteView(View):                                                            # view class to delete stock
    template_name = "delete_stock.html"                                                 # 'delete_stock.html' used as the template
    success_message = "Stock has been deleted successfully"                             # displays message when form is submitted
    
    def get(self, request, pk):
        stock = get_object_or_404(Stock, pk=pk)
        return render(request, self.template_name, {'object' : stock})

    def post(self, request, pk):  
        stock = get_object_or_404(Stock, pk=pk)
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