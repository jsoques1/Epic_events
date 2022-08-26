from rest_framework import routers
from django.urls import path, include

from .views import CustomerViewSet, ContractViewSet, EventViewSet

crm_router = routers.SimpleRouter()
crm_router.register('customers', CustomerViewSet, basename='customers')
crm_router.register('contracts', ContractViewSet, basename='contracts')
crm_router.register('events', EventViewSet, basename='events')


urlpatterns = [
    path('', include(crm_router.urls)),
]
