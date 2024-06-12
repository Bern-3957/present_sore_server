from rest_framework import serializers

from .models import Products, Cart, Gallery, Orders, OrderDetails


class GalleryModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ('id', 'image', 'product')

class ProductSerializer(serializers.ModelSerializer):
    images = GalleryModelSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ('id', 'title', 'price', 'vendor_code', 'is_published', 'description', 'created_at',
                  'quantity_in_stock', 'images')


class ProductsSerializer(serializers.ModelSerializer):
    images = GalleryModelSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ('id', 'title', 'price', 'vendor_code',
                  'is_published', 'images', 'is_edible', 'purpose', 'package')
class CartSerializer(serializers.ModelSerializer):
    product_details = ProductsSerializer(source='product', read_only=True)

    class Meta:
        model = Cart
        fields = ('__all__')

class ProductsForOrdersPageSerializer(serializers.ModelSerializer):
    images = GalleryModelSerializer(many=True, read_only=True)
    class Meta:
        model = Products
        fields = ('id', 'title', 'price', 'vendor_code','images')


class OrderDetailsSerializer(serializers.ModelSerializer):
    product = ProductsForOrdersPageSerializer()
    class Meta:
        model = OrderDetails
        fields = ('id', 'product', 'quantity')

class OrderSerializer(serializers.ModelSerializer):
    order_details = serializers.SerializerMethodField()

    class Meta:
        model = Orders
        fields = ('id', 'order_date', 'delivery_address', 'receive_method', 'order_status',
                  'delivey_cost', 'discount', 'final_cost', 'products_cost', 'order_details')

    def get_order_details(self, obj):
        order_details = OrderDetails.objects.filter(order=obj)
        return OrderDetailsSerializer(order_details, many=True).data

