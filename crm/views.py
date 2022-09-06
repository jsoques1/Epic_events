from datetime import date, datetime
from django.utils import timezone

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsManager
from .serializers import CustomerSerializer, ContractSerializer, EventSerializer
from .permissions import HasCustomerPermissions, HasContractPermissions, HasEventPermissions
from .models import Customer, Contract, Event
from users.models import User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from users.models import MGMT, SALES, SUPPORT
from rest_framework.viewsets import ModelViewSet
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
                    logger.error(f'The user {salesman} is not a salesmane')
                    raise ValidationError(f'The user {salesman} is not a salesman')
                # elif user != salesman:
                #     logger.error(f'The user {user} must be the salesman')
                #     raise ValidationError(f'The user {user} must be the salesman')


class CustomerViewSet(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated, IsManager | HasCustomerPermissions]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = ['^first_name', '^last_name', '^email', '^company_name']
    filterset_fields = ['is_signed']

    def get_queryset(self):
        customer_pk = self.kwargs.get("pk")
        if customer_pk:
            logger.info(f'Info for customer id {customer_pk} request by {self.request.user}')
        else:
            logger.info(f'Customer list request by {self.request.user}')
            self.queryset = Customer.objects.all()
            for customer in self.queryset:
                logger.info(customer)

        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        customer = Customer.objects.filter(company_name=request_data['company_name'])
        if customer.exists():
            logger.error(f'A customer {customer[0]} already exists')
            raise ValidationError(f'A customer {customer[0]} already exists')

        try:
            check_salesman(self.request)
        except Exception as e:
            logger.error(e)
            raise

        serializer = CustomerSerializer(data=request_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f'Customer {request_data["company_name"]} is added by {self.request.user}')
            return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_update(self, serializer, *args, **kwargs):
        instance = self.get_object()  # instance before update
        if serializer.is_valid(raise_exception=True):
            if instance.company_name != serializer.validated_data['company_name']:
                if Customer.objects.filter(company_name=serializer.validated_data['company_name']).exists():
                    logger.error(f'A customer {serializer.validated_data["company_name"]} already exists')
                    raise ValidationError(f'A customer {serializer.validated_data["company_name"]} already exists')

            try:
                check_salesman(self.request)
            except Exception as e:
                logger.error(e)
                raise

            serializer.save()
            logger.info(f'Customer {serializer.validated_data["company_name"]} updated by {self.request.user}')

    def destroy(self, request, *args, **kwargs):
        try:
            check_salesman(self.request)
        except Exception as e:
            logger.error(e)
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
    search_fields = ['^customer__first_name', '^customer__last_name', '^customer__email', '^customer__company_name']
    filterset_fields = ['is_signed']

    def get_queryset(self):
        contract_pk = self.kwargs.get("pk")
        if contract_pk:
            logger.info(f'Info for contract id {contract_pk} request by {self.request.user}')
        else:
            logger.info(f'Contract list request by {self.request.user}')
            self.queryset = Contract.objects.all()
            for contract in self.queryset:
                logger.info(contract)

        return self.queryset

    def perform_create(self, serializer, *args, **kwargs):
        request_data = self.request.data
        salesman = User.objects.get(id=request_data['salesman'])
        if salesman.role != SALES:
            logger.error(f"Salesman id#{salesman.id} {salesman.username} does not belong to the SALES team")
            raise ValidationError(f"Salesman id#{salesman.id} {salesman.username} does not belong to the SALES team")

        if serializer.is_valid(raise_exception=True):
            customer = serializer.validated_data['customer']
            is_signed = serializer.validated_data['is_signed']
            if not customer.is_signed:
                logger.error(f'The customer is still a prospect, sign him')
                raise ValidationError(f'The customer is still a prospect, sign him')
            if is_signed and not customer.is_signed:
                customer.is_signed = True
                logger.warning(f"contract #{serializer.data['id']} is signed, "
                               f"so the prospect {customer.username} is set automatically as a customer")
                customer.save()
            serializer.save()

        logger.info(f'Contract #{serializer.data["id"]} '
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
                logger.info(f'Contract #{instance.id} has been signed, so the customer is automatically signed also')
            if salesman != serializer.validated_data['salesman'] and self.request_user.role != MGMT:
                logger.error('Salesman reassignment can be done only by MGMT team')
                raise ValidationError('Salesman reassignment can be done only by MGMT team')
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
    filter_backends = [SearchFilter, DjangoFilterBackend]
    search_fields = [
        '^contract__customer__first_name', '^contract__customer__last_name', '^contract__customer__email',
        '^contract__customer__company_name', '^name', '^location'
    ]
    filterset_fields = ['is_completed']

    def get_queryset(self):
        event_pk = self.kwargs.get("pk")
        if event_pk:
            logger.info(f'Info for event id {event_pk} request by {self.request.user}')
            self.queryset = Event.objects.filter(id=int(event_pk))
        else:
            logger.info(f'Event list request by {self.request.user}')
            self.queryset = Event.objects.all()
            for event in self.queryset:
                logger.info(event)
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
            logger.error("Support must be assigned by the MGMT team")
            raise ValidationError("Support must be assigned by the MGMT team")
        elif self.request.user.role == MGMT and not request_data.get('support'):
            logger.warning("Support must be filled after creation by a manager")
        event_date = datetime.strptime(request_data['event_date'], "%Y-%m-%d %H:%M:%S")
        if event_date < timezone.now():
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

            if event_date < timezone.now():
                logger.error(f'Event date {event_date} is elapsed')
                raise ValidationError(f'Event date {event_date} is elapsed')
            support = serializer.validated_data.get('support')

            if support and self.request.user.role == MGMT:
                user = User.objects.filter(id=serializer.validated_data['support'].id)[0]
                if support and user.role != SUPPORT:
                    logger.error(f"Support id#{support.id} {user.username} "
                                 f"does not belong to the SUPPORT team")
                    raise ValidationError(f"Support id#{support.id} {user.username} "
                                          f"does not belong to the SUPPORT team")

            if event.support and event.support != support and self.request.user.role != MGMT:
                logger.error('Support (re)assignment can be done only by MGMT team')
                raise ValidationError('Support reassignment can be done only by MGMT team')

            if event.contract != serializer.validated_data['contract'] and self.request.user.role != MGMT:
                logger.error('Contract (re)assignment can be done only by MGMT team')
                raise ValidationError('Contract reassignment can be done only by MGMT team')
            serializer.save()
            logger.info(f'The event {name} at {event_date} updated by {self.request.user}')
            return Response({'message': f'Event {name} at {event_date} updated'}, status=status.HTTP_200_OK)

    def destroy(self, request, *args, **kwargs):
        event = self.get_object()
        name = event.name
        event_date = event.event_date
        user = User.objects.get(id=request.user.id)
        if user.role == SUPPORT and event.is_completed is False:
            logger.info(f"The event {name} at {event_date} is not yet completed")
            raise ValidationError(f"The event {name} at {event_date} is not yet completed")

        logger.info(f'Event {name} at {event_date} deleted by {self.request.user}')
        contract = event.contract
        event.delete()
        contract.delete()
        logger.warning(f'Event {name} has been deleted, the contract has been automatically deleted as well')
        return Response({'message': f'Event {name} at {event_date} deleted'}, status=status.HTTP_200_OK)
