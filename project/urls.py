from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView
from crm.views import CustomerViewSet

urlpatterns = [
    path('admin/', admin.site.urls),
    path("crm/", include("crm.urls")),
    path('', include('users.urls')),
    path("", TokenObtainPairView.as_view(), name="login"),
]
