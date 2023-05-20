from rest_framework import serializers
import bleach
from django.contrib.auth.models import User

from .models import MenuItem, Category, Cart, Order, OrderItem

# To manage users
class UserGroupsSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'groups']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'title']

class MenuItemSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = MenuItem
        fields = [
            'id', 'title', 'price', 'featured',
            'category', 'category_id'
        ]
    
        def validate(self, attrs):
            attrs['title'] = bleach.clean(attrs['title'])
            return super().validate(attrs)
        
class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = [
            'id', 'menuItem', 'quantity', 'unit_price', 'price'
        ]

# OrderSerializer For customers
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'delivery_crew', 'status', 'total', 'date'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'delivery_crew': {'read_only': True},
            'status': {'read_only': True},
            'total': {'read_only': True},
        }

# OrderSerializer For Manager
class ManagerOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'delivery_crew', 'status', 'total', 'date'
        ]

        extra_kwargs = {
            'user': {'read_only': True},
            'total': {'read_only': True},
            'date': {'read_only': True},
        }

# OrderSerializer For Delivery Crew
class DeliveryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = [
            'id', 'user', 'delivery_crew', 'status', 'total', 'date'
        ]
        extra_kwargs = {
            'user': {'read_only': True},
            'delivery_crew': {'read_only': True},
            'total': {'read_only': True},
            'date': {'read_only': True},
        }

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            'id', 'order', 'menuItem', 'quantity', 'unit_price', 'price'
        ]

    extra_kwargs = {
            'order': {'read_only': True},
            'menuItem': {'read_only': True},
            'quantity': {'read_only': True},
            'unit_price': {'read_only': True},
            'price': {'read_only': True},
        }