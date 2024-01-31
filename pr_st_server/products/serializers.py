from rest_framework import serializers

from .models import Products, Cart


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ('id', 'title', 'price', 'vendor_code')


class CartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = ('__all__')
