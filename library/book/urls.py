from django.urls import path
from .views import BookCreateView, BookUpdateView,BookListCreateView,BookDetailView

urlpatterns = [
    path('books/add/', BookCreateView.as_view(), name='book_add'),
    path('books/<int:pk>/edit/', BookUpdateView.as_view(), name='book_edit'),
    #API
    path('api/v1/book/', BookListCreateView.as_view(), name='book_list_create'),
    path('api/v1/book/<int:pk>/', BookDetailView.as_view(), name='book_detail'),
]
