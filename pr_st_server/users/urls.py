from django.urls import path

from .views import UserAPIView, DetailUserAPIView

urlpatterns = [
    path('user/', UserAPIView.as_view()),
    path('user/<int:pk>/', DetailUserAPIView.as_view()),  # new
]
