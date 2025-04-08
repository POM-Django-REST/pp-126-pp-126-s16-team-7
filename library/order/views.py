from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from .models import Order
from .forms import OrderForm,OrderUpdateForm
from .serializers import OrderSerializer
from book.models import Book
from django.utils import timezone


@user_passes_test(lambda u: u.role == 1)
def all_orders(request):
    orders = Order.objects.all()
    return render(request, 'order/all_orders.html', {'orders': orders})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'order/my_orders.html', {'orders': orders})


@login_required
def create_order(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            book = form.cleaned_data['book']
            plated_end_at = form.cleaned_data['plated_end_at']

            if book.count <= 0:
                return render(request, 'order/create_order.html', {
                    'form': form,
                    'error': 'Book is not available'
                })

            order = Order.create(user=request.user, book=book, plated_end_at=plated_end_at)
            if order:
                return redirect('my_orders')

        return render(request, 'order/create_order.html', {'form': form, 'error': 'Cannot create order'})

    else:
        form = OrderForm()
        return render(request, 'order/create_order.html', {'form': form})

@login_required
def update_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)

    if request.user != order.user and not request.user.is_staff:
        return redirect('my_orders')

    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('my_orders' if not request.user.is_staff else 'all_orders')

    else:
        form = OrderUpdateForm(instance=order)

    return render(request, 'order/update_order.html', {'form': form, 'order': order})

@user_passes_test(lambda u: u.role == 1)
def close_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    order.update(end_at=timezone.now())
    return redirect('all_orders')

class OrderListView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAdminUser]

class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'

class UserOrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)