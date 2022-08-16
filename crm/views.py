from rest_framework.permissions import IsAuthenticated, AllowAny
from .serializers import CustomerSerializer
from users.permissions import IsManager
from .permissions import HasCustomerPermissions
from .models import Customer
from users.models import User
from rest_framework import status

from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.utils import timezone
from rest_framework.viewsets import ModelViewSet

import logging
logger = logging.getLogger(__name__)


# class UserCreateView(CreateAPIView):
#     queryset = User.objects.all()
#     permission_classes = (IsAuthenticated, IsManager,)
#     serializer_class = UserSerializer
#
#     print('In UserCreateView')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsManager | HasCustomerPermissions]

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        customer = Customer.objects.filter(company_name=request_data['company_name'], email=request_data['email'])
        if customer.exists():
            raise ValidationError(f'A customer {customer} already exists')

        user = User.objects.get(id=self.request.user.id)

        serializer = CustomerSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.validated_data['salesman'] = user
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

