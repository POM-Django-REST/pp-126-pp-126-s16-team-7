from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    plated_end_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Planned End Date"
    )

    class Meta:
        model = Order
        fields = ['book', 'plated_end_at']


class OrderUpdateForm(forms.ModelForm):
    plated_end_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Planned End Date",
        required=False
    )
    end_at = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        label="Actual Return Date",
        required=False
    )

    class Meta:
        model = Order
        fields = ['plated_end_at', 'end_at']
