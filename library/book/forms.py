from django import forms
from .models import Book
from author.models import Author  

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['name', 'description', 'count', 'authors']
        widgets = {
            'authors': forms.CheckboxSelectMultiple()
        }
