import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Customer, Contract, Event
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status
from time import sleep
from collections import OrderedDict
import json
from django.core import serializers


class TestCustomer(APITestCase):
    @pytest.mark.django_db
    def setUp(self):

        User.objects.create_user(
            pk=1,
            username='mgr',
            password='mgr',
            role=MGMT,
        )

        User.objects.create_user(
            pk=2,
            username='sales1',
            password='sales1',
            role=SALES,
        )

        User.objects.create_user(
            pk=3,
            username='support1',
            password='support1',
            role=SUPPORT,
        )

        User.objects.create_user(
            pk=4,
            username='sales2',
            password='sales2',
            role=SALES,
        )

        User.objects.create_user(
            pk=5,
            username='support2',
            password='support2',
            role=SUPPORT,
        )

        call_command('loaddata', 'customers.json', verbosity=0)
        call_command('loaddata', 'contracts.json', verbosity=0)
        call_command('loaddata', 'events.json', verbosity=0)

    @pytest.mark.django_db
    def test_login_ok(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    @pytest.mark.django_db
    def test_get_customers_list(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get(url, format="json")
        print(response.data['results'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))

    @pytest.mark.django_db
    def test_get_customer_detail(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-detail", args=(1,))
        print(url)
        response = self.client.get(url, format="json")
        customer = Customer.objects.get(id=1)
        print('************************************')
        print(f'response={response}')
        print(f'response.data={response.data}')
        print(f'customer={customer}')
        print('************************************')


        # assuming obj is a model instance
        # serialized_obj = serializers.serialize('json', [customer, ])
        # print(serialized_obj)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(len(response), 1)
        # self.assertEqual(response.data, serialized_obj)

    # @pytest.mark.django_db
    # def test_wait_1h(self):
    #     sleep(3600)
