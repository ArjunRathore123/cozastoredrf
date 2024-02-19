from rest_framework import serializers
from .models import Category,Product,Cart,Order

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields='__all__'

class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model=Cart
        fields='__all__'

class OrderSerialzier(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'