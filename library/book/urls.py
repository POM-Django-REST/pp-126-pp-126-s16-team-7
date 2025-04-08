from django.urls import path
from .views import BookCreateView, BookUpdateView

urlpatterns = [
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
]
