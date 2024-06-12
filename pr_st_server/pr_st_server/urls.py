
from django.contrib import admin
from django.urls import path, re_path, include

from django.conf import settings
from products.views import ProductAPIView, CategoryAPIView, CartAPIView, ProductDetailAPIView, GalleryListCreate, \
    OrderAPIView
from users.views import UserAPIView, DetailUserAPIView
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api/v1/products-app/', include('products.urls')),
    path('api/v1/users-app/', include('users.urls')),

    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
