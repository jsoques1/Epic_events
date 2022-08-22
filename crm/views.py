from datetime import date, datetime
from django.utils import timezone

from rest_framework.permissions import IsAuthenticated
from users.permissions import IsManager
from .serializers import CustomerSerializer, ContractSerializer, EventSerializer
from .permissions import HasCustomerPermissions, HasContractPermissions, HasEventPermissions
from .models import Customer, Contract, Event
from users.models import User
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from rest_framework.viewsets import ModelViewSet
from users.models import MGMT, SALES, SUPPORT

import logging
logger = logging.getLogger(__name__)


def check_salesman(request):
    request_data = request.data
    user = User.objects.get(id=request.user.id)
    if user.role in [SALES, MGMT]:
        if request_data.get('salesman'):
            salesman = User.objects.filter(id=request_data['salesman'])
            if salesman.exists():
                salesman = salesman[0]
                if salesman.role != SALES:
                    logger.error(f'The salesman {salesman} is invalid')
                    raise ValidationError(f'The salesman {salesman} is invalid')
                elif user != salesman:
                    logger.error(f'The user {user} must be the salesman')
                    raise ValidationError(f'The user {user} must be the salesman')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsManager | HasCustomerPermissions]

    def get_queryset(self):
        customer_pk = self.kwargs.get("pk")
        if customer_pk:
            if not Customer.objects.filter(id=customer_pk).exists():
                logger.error(f'No customer with id {customer_pk} exists')
                raise ValidationError(f'No customer with id {customer_pk} exists')
        else:
            self.queryset = Customer.objects.all()

        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        customer = Customer.objects.filter(company_name=request_data['company_name'])
        if customer.exists():
            logger.error(f'A customer {customer} already exists')
            raise ValidationError(f'A customer {customer} already exists')

        try:
            check_salesman(self.request)
        except Exception as e:
            raise

        serializer = CustomerSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'Customer {request_data["company_name"]} is added by {self.request.user}')
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        instance = self.get_object()  # instance before update
        print(instance)
        print(serializer.validated_data['company_name'])
        if serializer.is_valid(raise_exception=True):
            if instance.company_name != serializer.validated_data['company_name']:
                if Customer.objects.filter(company_name=serializer.validated_data['company_name']).exists():
                    logger.error(f'A customer {serializer.validated_data["company_name"]} already exists')
                    raise ValidationError(f'A customer {serializer.validated_data["company_name"]} already exists')

            try:
                check_salesman(self.request)
            except Exception as e:
                raise

            serializer.save()
            logger.info(f'Customer {serializer.validated_data["company_name"]} updated by {self.request.user}')

    def destroy(self, request, *args, **kwargs):
        try:
            check_salesman(self.request)
        except Exception as e:
            raise

        customer = self.get_object()
        company_name = customer.company_name
        customer.delete()
        logger.info(f'Customer {company_name} is deleted by {self.request.user}')
        return Response({'message': f'Customer {company_name} deleted'}, status=status.HTTP_200_OK)


class ContractViewSet(ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer
    permission_classes = [IsAuthenticated, IsManager | HasContractPermissions]

    def get_queryset(self):
        contract_pk = self.kwargs.get("pk")
        if contract_pk:
            if not Contract.objects.filter(id=contract_pk).exists():
                logger.error(f'No contract #{contract_pk} exists')
                raise ValidationError(f'No contract #{contract_pk} exists')
        else:
            self.queryset = Contract.objects.all()

        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        salesman = Contract.objects.get(salesman=request_data['salesman'])
        if salesman.role != SALES:
            logger.error(f"Salesman id#{salesman.id} {salesman.username} does not belong to the SALES team")
            raise ValidationError(f"Salesman id#{salesman.id} {salesman.username} does not belong to the SALES team")
        
        if serializer.is_valid(raise_exception=True):
            customer = serializer.validated_data['customer']
            is_signed = serializer.validated_data['is_signed']
            if is_signed and not customer.is_signed:
                customer.is_signed = True
                customer.save()
            serializer.save()

        logger.info(f'Contract #{serializer.validated_data["id"]} '
                    f'{serializer.validated_data["customer"]} added by {self.request.user}')
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        instance = self.get_object()  # instance before update
        salesman = instance.salesman
        if serializer.is_valid(raise_exception=True):
            customer = serializer.validated_data['customer']
            payment_due = serializer.validated_data['payment_due']
            is_signed = serializer.validated_data['is_signed']
            if payment_due < date.today():
                logger.error(f'Payment due {payment_due} is elapsed')
                raise ValidationError(f'Payment due {payment_due} is elapsed')
            if is_signed and not customer.is_signed:
                customer.is_signed = True
            if salesman != serializer.validated_data['salesman'] and self.request_user.role != MGMT:
                logger.error(f'Salesman reassignment can be done only by MGMT team')
                raise ValidationError(f'Salesman reassignment can be done only by MGMT team')
            customer.save()
            serializer.save()
            logger.info(f'Contract #{instance.id} '
                        f'{serializer.validated_data["customer"]} updated by {self.request.user}')

    def destroy(self, request, *args, **kwargs):
        contract = self.get_object()
        company_name = contract.customer.company_name
        contract_id = contract.id
        logger.info(f'Contract #{contract_id} {company_name} deleted by {self.request.user}')
        contract.delete()
        return Response({'message': f'Contract #{contract_id} {company_name} deleted'}, status=status.HTTP_200_OK)


class EventViewSet(ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated, IsManager | HasEventPermissions]

    def get_queryset(self):
        event_pk = self.kwargs.get("pk")
        if event_pk:
            if not Event.objects.filter(id=event_pk).exists():
                logger.error(f'No event #{event_pk} exists')
                raise ValidationError(f'No event #{event_pk} exists')
        else:
            self.queryset = Event.objects.all()

        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        event = Event.objects.filter(contract=request_data['contract'])
        if event.exists():
            logger.error(f"An event for contract #{request_data['contract'].id} already exists")
            raise ValidationError(f"An event for contract #{request_data['contract'].id} already exists")

        contract = Event.objects.filter(support=request_data['contract'])
        if contract.exists() and not contract[0].is_signed:
            logger.error(f"{request_data['contract']} for event {request_data['name']}"
                         f"at {request_data['name']} is not signed yet")
            raise ValidationError(f"{request_data['contract']} for event {request_data['name']}"
                                  f"at {request_data['name']} is not signed yet")

        if self.request.user.role != MGMT and request_data.get('support'):
            logger.error(f"Support must be assigned by the MGMT team")
            raise ValidationError(f"Support must be assigned by the MGMT team")
        elif self.request.user.role == MGMT and not request_data.get('support'):
            logger.error(f"Support must be filled")
            raise ValidationError(f"Support must be filled")
        elif request_data.get('support'):
            support = Event.objects.filter(support=request_data['support'])
            if support.exists() and support.role != SUPPORT:
                logger.error(f"Support id#{support.id} {support.username} "
                             f"does not belong to the SUPPORT team")
                raise ValidationError(f"Support id#{support.id} {support.username} "
                                      f"does not belong to the SUPPORT team")

        if datetime.strptime(request_data['event_date'], '%Y-%m-%d %H:%M:%S') < timezone.now():
            logger.error(f'Event date {request_data["event_date"]} is elapsed')
            raise ValidationError(f'Event date {request_data["event_date"]} is elapsed')

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'Event {serializer.data["name"]}'
                        f'{serializer.data["event_date"]} added by {self.request.user}')

        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):

        event = self.get_object()  # instance before update
        if serializer.is_valid(raise_exception=True):
            name = serializer.validated_data['name']
            event_date = serializer.validated_data['event_date']
            print(event_date)
            if event_date < timezone.now():
                logger.error(f'Event date {event_date} is elapsed')
                raise ValidationError(f'Event date {event_date} is elapsed')
            support = serializer.validated_data.get('support')
            if event.support != support and self.request.user.role != MGMT:
                logger.error(f'Contract reassignment can be done only by MGMT team')
                raise ValidationError(f'Support reassignment can be done only by MGMT team')
            if event.contract != serializer.validated_data['contract'] and self.request.user.role != MGMT:
                logger.error(f'Contract reassignment can be done only by MGMT team')
                raise ValidationError(f'Contract reassignment can be done only by MGMT team')
            serializer.save()
            logger.info(f'The event {name} at {event_date} updated by {self.request.user}')

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        name = event.name
        event_date = event.event_date
        user = User.objects.get(id=request.user.id)
        if user.role == SALES and event.is_completed is False:
            logger.info(f"The event {name} at {event_date} is not set as completed")
            raise ValidationError(f"The event {name} at {event_date} is not set as completed")

        logger.info(f'Event {name} at {event_date} deleted by {self.request.user}')
        event.delete()
        return Response({'message': f'Event {name} at {event_date} deleted'}, status=status.HTTP_200_OK)
