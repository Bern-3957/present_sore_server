from django.forms import model_to_dict
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from .models import Products, Categories, Cart
from .serializers import ProductSerializer, CartSerializer


class ProductAPIView(APIView):
    def get(self, request):
        lst = Products.objects.all().values()
        return Response({'products': list(lst)})

    def post(self, request):
        print(request)
        new_product = Products.objects.create(
            title=request.data['title'],
            description=request.data['description'],
            price=int(request.data['price']),
            is_published=request.data['is_published'],
            category_id=request.data['category_id'],
        )
        return Response({'product': model_to_dict(new_product)})


# class ProductAPIView(generics.ListAPIView):
#     queryset = Products.objects.all()
#     serializer_class = ProductSerializer


class CategoryAPIView(APIView):
    def get(self, request):
        lst = Categories.objects.all().values()
        return Response({'categories': list(lst)})


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):

        cart_items = Cart.objects.filter(user=request.user)
        cart_serializer = CartSerializer(cart_items, many=True)

        products = [items.product for items in cart_items]
        product_serializer = ProductSerializer(products, many=True)

        return Response({
            'carts': list(cart_serializer.data),
            'carts_products': list(product_serializer.data)
        })

    def post(self, request):
        product = get_object_or_404(Products, pk=int(request.data.get('product_id')))

        new_product_in_cart = Cart.objects.create(
            user=request.user,
            product=product,
            quantity=int(request.data.get('quantity', 1))
        )
        return Response({'cart': model_to_dict(new_product_in_cart)})

    def delete(self, request, cart_id):
        Cart.objects.get(user=request.user, pk=(cart_id)).delete()
        return Response(f"Cart with id {cart_id} delete from cart_list")
