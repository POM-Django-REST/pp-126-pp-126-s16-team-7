from rest_framework import serializers
from .models import CustomUser
from order.models import Order
from book.serializers import BookSerializer 
from book.models import Book
class OrderSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    plated_end_at = serializers.DateTimeField(required=True)

    class Meta:
        model = Order
        fields = ['id', 'book', 'user', "plated_end_at"]

    def create(self, validated_data):
        user_id = self.context['request'].user.id
        validated_data.pop('user', None)
        plated_end_at = validated_data.get('plated_end_at')
        if plated_end_at is None:
            raise serializers.ValidationError("The 'plated_end_at' field is required.")
        order = Order.objects.create(user_id=user_id, **validated_data)
        return order

class CustomUserSerializer(serializers.ModelSerializer):
    orders = OrderSerializer(many=True, read_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'first_name', 'last_name', 'email', 'role', 'is_active', 'orders')

class CustomUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=False)

    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'email', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = CustomUser(**validated_data)
        if password:
            user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.get('password', None)
        if password:
            instance.set_password(password) 
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance