from django.urls import path
from .views import AuthorCreateView, AuthorUpdateView, AuthorListCreateView, AuthorDetailView

urlpatterns = [
    path('authors/add/', AuthorCreateView.as_view(), name='author_add'),
    path('authors/<int:pk>/edit/', AuthorUpdateView.as_view(), name='author_edit'),
    path('api/v1/authors/', AuthorListCreateView.as_view(), name='api_all_authors'),
    path('api/v1/author/<int:id>/', AuthorDetailView.as_view(), name='api_author_detail')

]
