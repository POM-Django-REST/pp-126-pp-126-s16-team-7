from rest_framework import serializers
from book.models import Book
from order.models import Order
from book.serializers import BookSerializer

class OrderSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())

    class Meta:
        model = Order
        fields = ('id', 'book', 'user', 'created_at', 'end_at', 'plated_end_at')