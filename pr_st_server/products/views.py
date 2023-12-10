from django.forms import model_to_dict
from django.shortcuts import render
from rest_framework import generics
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Products
from .serializers import ProductSerializer


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
