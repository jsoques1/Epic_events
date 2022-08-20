# from rest_framework_nested import routers
from rest_framework import routers
from django.urls import path, include

from .views import CustomerViewSet, ContractViewSet, EventViewSet

crm_router = routers.SimpleRouter()
crm_router.register('customers', CustomerViewSet, basename='customers')
crm_router.register('contracts', ContractViewSet, basename='contracts')
crm_router.register('events', EventViewSet, basename='events')
# contracts = routers.NestedSimpleRouter(router, r'clients', lookup='clients')
# clients.register('contracts', ClientsViewSet, basename='contracts')

# contracts = routers.NestedSimpleRouter(projects, r'contracts', lookup='contracts')
# contracts.register('events', ClientsViewSet, basename='events')


urlpatterns = [
    path('', include(crm_router.urls)),
    # path('', include(clients.urls)),
    # path('', include(contracts.urls)),
]
