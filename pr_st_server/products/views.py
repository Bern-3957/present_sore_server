from itertools import product

from django.forms import model_to_dict
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from rest_framework import generics
# Create your views here.
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny

from users.models import Users
from .models import Products, Categories, Cart, Gallery, Orders, OrderDetails
from .serializers import ProductsSerializer, CartSerializer, ProductSerializer, GalleryModelSerializer, OrderSerializer


class ProductAPIView(APIView):

    def get(self, request):
        # lst = Products.objects.all().values()
        lst = Products.objects.filter(is_published=True)
        serializer = ProductsSerializer(lst, many=True)
        return Response({'products': list(serializer.data)})

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


class ProductDetailAPIView(generics.RetrieveAPIView):
    queryset = Products.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def get_object(self):
        return Products.objects.get(id=self.kwargs.get('product_id'))


class GalleryListCreate(APIView):
    def get(self, request, product_id):
        lst = Gallery.objects.filter(product=product_id)
        serializer_lst = GalleryModelSerializer(lst, many=True)

        return Response(serializer_lst.data)


class CategoryAPIView(APIView):
    def get(self, request):
        lst = Categories.objects.all().values()
        return Response({'categories': list(lst)})


class CartAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        print(request)
        cart_items = Cart.objects.filter(user=request.user)
        cart_serializer = CartSerializer(cart_items, many=True)
        response_data = {
            'user_id': request.user.id,
            'cart_items': cart_serializer.data,
        }

        return Response(response_data)
    def post(self, request):
        product = get_object_or_404(Products, pk=int(request.data.get('product_id')))
        print('---',product)
        userCart = Cart.objects.filter(user=request.user, product=product)

        if not userCart.exists():
            new_product_in_cart = Cart.objects.create(
                user=request.user,
                product=product,
                quantity=int(request.data.get('quantity', 1))
            )
            return Response({'cart': model_to_dict(new_product_in_cart)})
        return Response({'cart': 'Такой товар уже есть в корзине'})

    def delete(self, request, cart_id=None):
        if cart_id is not None:
            cart = Cart.objects.get(user=request.user, pk=(cart_id))
            try:
                cart.delete()
                return Response({'message': "Cart with id {cart_id} delete from cart_list"}, status=status.HTTP_204_NO_CONTENT)
            except cart.DoesNotExist:
                return Response({'message':"Cart with id {cart_id} not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            Cart.objects.filter(user=request.user).delete()
            return Response("All carts deleted successfully", status=status.HTTP_204_NO_CONTENT)
    def patch(self, request, cart_id):
        try:
            cart_item = Cart.objects.get(user=request.user, pk=(cart_id))
        except:
            return Response({'error': 'Товар не найден в корзине'}, status=status.HTTP_404_NOT_FOUND)
        new_quantity = int(request.data.get('quantity', 1))
        cart_item.quantity = new_quantity
        cart_item.save()
        return Response(f"Quatity cart with id {cart_id} changed")


class OrderAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            orders = Orders.objects.filter(user=request.user)
            orders = OrderSerializer(orders, many=True)
            if len(orders.data) == 0:
                return Response({'message': 'У пользователя нет заказов', 'orders': orders.data},
                                status=status.HTTP_200_OK)
            else:
                return Response({'message': 'Заказы пользователя успешно найдены', 'orders': orders.data}, status=status.HTTP_200_OK)
        except Orders.DoesNotExist:
            return Response({'message': 'Что-то пошло не так'}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request):
        print('--------------', request.data)

        orderInfo = request.data['order']['orderInfo']
        cartMoney = request.data['order']['cartMoney']
        orderItems = request.data['order']['orderItems']
        # delivery_address = f"{orderInfo['town']}-{orderInfo['street']}-{orderInfo['house']}-{orderInfo['entrance']}-{orderInfo['apartment']}"

        new_order = Orders.objects.create(user=request.user,
                              delivery_address=orderInfo['address'],
                              receive_method=orderInfo['order_receive_method'],
                              order_status=Orders.OrderStatus.IN_PROCESSING,
                              delivey_cost=cartMoney['deliveryCost'],
                              discount=cartMoney['discount'],
                              final_cost=cartMoney['finalCost'],
                              products_cost=cartMoney['productsCost']
                              )

        objects_to_create = [OrderDetails(order=new_order, product=Products.objects.get(id=item['product_id']), quantity=item['quantity']) for item in orderItems]

        OrderDetails.objects.bulk_create(objects_to_create)
        return Response({"message": "Заказ успешно оформлен"}, status=status.HTTP_201_CREATED)



# class CartAPIView(APIView):
#     permission_classes = [IsAuthenticated]
#
#     def get(self, request):
#         """Взять все товары в корзине данного пользователя"""

#
# cart_items = Cart.objects.filter(user=request.user)
# cart_serializer = CartSerializer(cart_items, many=True)
#
# products = [items.product for items in cart_items]
# product_serializer = ProductSerializer(products, many=True)
#
# return Response({
#     'carts': list(cart_serializer.data),
#     'carts_products': list(product_serializer.data)
# })

# try:
#     cart_items = Cart.objects.filter(user=request.user)
#     items_list = []
#     for cart_item in cart_items:
#         product_info = {
#             'cart_id': cart_item.id,
#             'product_id': cart_item.product.id,
#             'quantity': cart_item.quantity,
#             'product_details': {
#                 'title': cart_item.product.title,
#                 'price': cart_item.product.price,
#                 'vendor_code': cart_item.product.vendor_code,
#             }
#         }
#         items_list.append(product_info)
#
#     response_data = {
#         'user_id': request.user.id,
#         'cart_items': items_list,
#     }
#     return JsonResponse(response_data, safe=False)
# except Users.DoesNotExist:
#     return JsonResponse({'error': 'Пользователь не найден'}, status=404)
