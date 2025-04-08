from django.views.generic import CreateView, UpdateView
from django.urls import reverse_lazy
from .models import Author
from .forms import AuthorForm
from authentication.views import get_current_user
from django.http import HttpResponse
from .serializers import AuthorSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

class AuthorAccessMixin:
    def dispatch(self, request, *args, **kwargs):
        current_user = get_current_user(request)
        if not current_user or current_user.role != 1:
            return HttpResponse("Access denied. Librarians only.")
        return super().dispatch(request, *args, **kwargs)

class AuthorCreateView(AuthorAccessMixin, CreateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = reverse_lazy('authors_list')

class AuthorUpdateView(AuthorAccessMixin, UpdateView):
    model = Author
    form_class = AuthorForm
    template_name = 'author_form.html'
    success_url = reverse_lazy('authors_list')


class AuthorListCreateView(generics.ListCreateAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  

    def perform_create(self, serializer):
        serializer.save()

class AuthorDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]  
    lookup_field = 'id'