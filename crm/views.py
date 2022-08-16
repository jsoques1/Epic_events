from rest_framework.permissions import IsAuthenticated
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
from users.models import SALES, SUPPORT

import logging
logger = logging.getLogger(__name__)


def check_customer_salesman(request):
    request_data = request.data
    user = User.objects.get(id=request.user.id)
    if user.role == SALES:
        if request_data.get('salesman'):
            salesman = User.objects.filter(id=request_data['salesman'])
            if salesman.exists():
                salesman = salesman[0]
                if salesman.role != SALES:
                    raise ValidationError(f'The salesman {salesman} is invalid')
                elif user != salesman:
                    raise ValidationError(f'The user {user} must be the salesman')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsManager | HasCustomerPermissions]

    def get_queryset(self):
        customer_pk = self.kwargs.get("pk")
        if customer_pk:
            self.queryset = Customer.objects.filter(id=customer_pk)
        else:
            self.queryset = Customer.objects.all()

        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        customer = Customer.objects.filter(company_name=request_data['company_name'])
        if customer.exists():
            raise ValidationError(f'A customer {customer} already exists')

        try:
            check_customer_salesman(self.request)
        except Exception as e:
            raise

        serializer = CustomerSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'Customer {request_data["company_name"]} added by {self.request.user}')
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        instance = self.get_object()  # instance before update
        if serializer.is_valid(raise_exception=True):
            print(instance.company_name)
            print(serializer.validated_data['company_name'])
            if instance.company_name != serializer.validated_data['company_name']:
                if Customer.objects.filter(company_name=serializer.validated_data['company_name']).exists():
                    raise ValidationError(f'A customer {serializer.validated_data["company_name"]} already exists')

            try:
                check_customer_salesman(self.request)
            except Exception as e:
                raise

            # user = User.objects.get(id=self.request.user.id)
            # request_data = self.request.data
            # if user.role == SALES:
            #     if request_data.get('salesman'):
            #         salesman = User.objects.filter(id=request_data['salesman'])
            #         if salesman.role != SALES:
            #             raise ValidationError(f'The salesman {salesman} is invalid')
            #         elif user != salesman:
            #             raise ValidationError(f'The user {user} must be the salesman')

            serializer.save()
            logger.info(f'Customer {serializer.validated_data["company_name"]} updated by {self.request.user}')

    def destroy(self, request, *args, **kwargs):
        # customer_id = self.kwargs['pk']
        # customer = Customer.objects.filter(id=customer_id)
        # if not customer.exists():
        #     raise ValidationError('Customer not found')

        # request_data = self.request.data
        # user = User.objects.get(id=self.request.user.id)
        # if user.role == SALES:
        #     if request_data.get('salesman'):
        #         salesman = User.objects.filter(id=request_data['salesman'])
        #         if salesman.role != SALES:
        #             raise ValidationError(f'The salesman {salesman} is invalid')
        #         elif user != salesman:
        #             raise ValidationError(f'The user {user} must be the salesman')

        try:
            check_customer_salesman(self.request)
        except Exception as e:
            raise

        customer = self.get_object()
        company_name = customer.company_name
        customer.delete()
        logger.info(f'Customer {company_name} by {self.request.user}')
        return Response({'message': f'Customer {company_name} deleted'}, status=status.HTTP_200_OK)
