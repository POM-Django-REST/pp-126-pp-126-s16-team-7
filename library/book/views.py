from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Book
from order.models import Order
from authentication.models import CustomUser  
from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .forms import BookForm
from authentication.views import get_current_user
from django.http import HttpResponse
from rest_framework import generics
from .serializers import BookSerializer

@login_required
def book_list(request):
    books = Book.objects.all()

    title = request.GET.get('title')
    author = request.GET.get('author')

    if title:
        books = books.filter(name__icontains=title)

    if author:
        books = books.filter(authors__name__icontains=author)

    return render(request, 'book/book_list.html', {'books': books})


@login_required
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'book/book_detail.html', {'book': book})


@user_passes_test(lambda u: u.is_staff)
def books_by_user(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)

    orders = Order.objects.filter(user=user, end_at=None)
    books = [order.book for order in orders]

    return render(request, 'book/user_books.html', {
        'user': user,
        'books': books
    })

class BookAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user or current_user.role != 1:
            return HttpResponse("Access denied. Librarians only.")
        return super().dispatch(request, *args, **kwargs)

class BookCreateView(BookAccessMixin, CreateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('books_list')

class BookUpdateView(BookAccessMixin, UpdateView):
    model = Book
    form_class = BookForm
    template_name = 'book/book_form.html'
    success_url = reverse_lazy('books_list')


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer