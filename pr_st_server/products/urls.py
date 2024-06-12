
from django.urls import path

from .views import ProductAPIView, CategoryAPIView, CartAPIView, ProductDetailAPIView, GalleryListCreate, OrderAPIView

urlpatterns = [
    path('products/', ProductAPIView.as_view()),
    path('product/<int:product_id>/', ProductDetailAPIView.as_view()),
    path('categories/', CategoryAPIView.as_view()),
    path('cart/', CartAPIView.as_view()),
    path('cart/delete-all-carts/', CartAPIView.as_view()),
    path('cart/<int:cart_id>/', CartAPIView.as_view()),
    path('images/<int:product_id>/', GalleryListCreate.as_view()),
    path('order/', OrderAPIView.as_view()),
]