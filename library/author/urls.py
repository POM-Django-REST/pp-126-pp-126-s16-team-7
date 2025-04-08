from django.urls import path
from .views import AuthorCreateView, AuthorUpdateView

urlpatterns = [
    path('authors/add/', AuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_edit'),
]
