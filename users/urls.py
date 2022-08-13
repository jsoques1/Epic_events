from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from .views import UserViewSet

users_router = routers.DefaultRouter()
users_router.register("users/", UserViewSet, basename='users')


urlpatterns = [
    path("", TokenObtainPairView.as_view(), name="login"),
    path("", include(users_router.urls)),
]
