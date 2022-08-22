import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Customer
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status
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

    # @pytest.mark.django_db
    # def test_login_ok(self):
    #     url = reverse("login")
    #     data = {"username": 'mgr', "password": 'mgr'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue("access" in response.data)
    #     self.assertTrue("refresh" in response.data)
    #
    # @pytest.mark.django_db
    # def test_1_manager_get_customers_list(self):
    #     url = reverse("login")
    #     data = {"username": 'mgr', "password": 'mgr'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #
    #     url = reverse("customers-list")
    #     response = self.client.get(url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
    #     for customer in response.data['results']:
    #         customer = dict(customer)
    #         db_customer = Customer.objects.get(id=customer['id'])
    #         serialized_obj = serializers.serialize('json', [db_customer, ])
    #         res = json.loads(serialized_obj)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(customer['id'], res[0]['pk'])
    #         serialized_fields = res[0]['fields']
    #         self.assertEqual(customer['first_name'], serialized_fields['first_name'])
    #         self.assertEqual(customer['last_name'], serialized_fields['last_name'])
    #         self.assertEqual(customer['email'], serialized_fields['email'])
    #         self.assertEqual(customer['company_name'], serialized_fields['company_name'])
    #         self.assertEqual(customer['phone_number'], serialized_fields['phone_number'])
    #         self.assertEqual(customer['mobile_number'], serialized_fields['mobile_number'])
    #         self.assertEqual(customer['is_signed'], serialized_fields['is_signed'])
    #         self.assertEqual(customer['salesman'], serialized_fields['salesman'])
    #
    # @pytest.mark.django_db
    # def test_1_sales_get_customers_list(self):
    #     url = reverse("login")
    #     data = {"username": 'sales1', "password": 'sales1'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #
    #     url = reverse("customers-list")
    #     response = self.client.get(url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
    #     for customer in response.data['results']:
    #         customer = dict(customer)
    #         db_customer = Customer.objects.get(id=customer['id'])
    #         serialized_obj = serializers.serialize('json', [db_customer, ])
    #         res = json.loads(serialized_obj)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(customer['id'], res[0]['pk'])
    #         serialized_fields = res[0]['fields']
    #         self.assertEqual(customer['first_name'], serialized_fields['first_name'])
    #         self.assertEqual(customer['last_name'], serialized_fields['last_name'])
    #         self.assertEqual(customer['email'], serialized_fields['email'])
    #         self.assertEqual(customer['company_name'], serialized_fields['company_name'])
    #         self.assertEqual(customer['phone_number'], serialized_fields['phone_number'])
    #         self.assertEqual(customer['mobile_number'], serialized_fields['mobile_number'])
    #         self.assertEqual(customer['is_signed'], serialized_fields['is_signed'])
    #         self.assertEqual(customer['salesman'], serialized_fields['salesman'])
    #
    # @pytest.mark.django_db
    # def test_1_support_get_customers_list(self):
    #     url = reverse("login")
    #     data = {"username": 'support1', "password": 'support1'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #
    #     url = reverse("customers-list")
    #     response = self.client.get(url, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
    #     for customer in response.data['results']:
    #         customer = dict(customer)
    #         db_customer = Customer.objects.get(id=customer['id'])
    #         serialized_obj = serializers.serialize('json', [db_customer, ])
    #         res = json.loads(serialized_obj)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(customer['id'], res[0]['pk'])
    #         serialized_fields = res[0]['fields']
    #         self.assertEqual(customer['first_name'], serialized_fields['first_name'])
    #         self.assertEqual(customer['last_name'], serialized_fields['last_name'])
    #         self.assertEqual(customer['email'], serialized_fields['email'])
    #         self.assertEqual(customer['company_name'], serialized_fields['company_name'])
    #         self.assertEqual(customer['phone_number'], serialized_fields['phone_number'])
    #         self.assertEqual(customer['mobile_number'], serialized_fields['mobile_number'])
    #         self.assertEqual(customer['is_signed'], serialized_fields['is_signed'])
    #         self.assertEqual(customer['salesman'], serialized_fields['salesman'])
    #
    # @pytest.mark.django_db
    # def test_2_manager_get_customer_detail(self):
    #     url = reverse("login")
    #     data = {"username": 'mgr', "password": 'mgr'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #     for customer_id in range(1, 6):
    #         url = reverse("customers-detail", args=(customer_id,))
    #         response = self.client.get(url, format="json")
    #         customer = Customer.objects.get(id=customer_id)
    #
    #         serialized_obj = serializers.serialize('json', [customer, ])
    #         res = json.loads(serialized_obj)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(response.data['id'], res[0]['pk'])
    #         serialized_fields = res[0]['fields']
    #         self.assertEqual(response.data['first_name'], serialized_fields['first_name'])
    #         self.assertEqual(response.data['last_name'], serialized_fields['last_name'])
    #         self.assertEqual(response.data['email'], serialized_fields['email'])
    #         self.assertEqual(response.data['company_name'], serialized_fields['company_name'])
    #         self.assertEqual(response.data['phone_number'], serialized_fields['phone_number'])
    #         self.assertEqual(response.data['mobile_number'], serialized_fields['mobile_number'])
    #         self.assertEqual(response.data['is_signed'], serialized_fields['is_signed'])
    #         self.assertEqual(response.data['salesman'], serialized_fields['salesman'])
    #
    # def test_2_sales_get_customer_detail(self):
    #     url = reverse("login")
    #     data = {"username": 'sales1', "password": 'sales1'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #     for customer_id in range(1, 6):
    #         url = reverse("customers-detail", args=(customer_id,))
    #         response = self.client.get(url, format="json")
    #         customer = Customer.objects.get(id=customer_id)
    #
    #         serialized_obj = serializers.serialize('json', [customer, ])
    #         res = json.loads(serialized_obj)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(response.data['id'], res[0]['pk'])
    #         serialized_fields = res[0]['fields']
    #         self.assertEqual(response.data['first_name'], serialized_fields['first_name'])
    #         self.assertEqual(response.data['last_name'], serialized_fields['last_name'])
    #         self.assertEqual(response.data['email'], serialized_fields['email'])
    #         self.assertEqual(response.data['company_name'], serialized_fields['company_name'])
    #         self.assertEqual(response.data['phone_number'], serialized_fields['phone_number'])
    #         self.assertEqual(response.data['mobile_number'], serialized_fields['mobile_number'])
    #         self.assertEqual(response.data['is_signed'], serialized_fields['is_signed'])
    #         self.assertEqual(response.data['salesman'], serialized_fields['salesman'])
    #
    # def test_2_support_get_customer_detail(self):
    #     url = reverse("login")
    #     data = {"username": 'support1', "password": 'support1'}
    #     response = self.client.post(url, data, format="json")
    #     self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
    #     for customer_id in range(1, 6):
    #         url = reverse("customers-detail", args=(customer_id,))
    #         response = self.client.get(url, format="json")
    #         customer = Customer.objects.get(id=customer_id)
    #
    #         serialized_obj = serializers.serialize('json', [customer, ])
    #         res = json.loads(serialized_obj)
    #
    #         self.assertEqual(response.status_code, status.HTTP_200_OK)
    #         self.assertEqual(response.data['id'], res[0]['pk'])
    #         serialized_fields = res[0]['fields']
    #         self.assertEqual(response.data['first_name'], serialized_fields['first_name'])
    #         self.assertEqual(response.data['last_name'], serialized_fields['last_name'])
    #         self.assertEqual(response.data['email'], serialized_fields['email'])
    #         self.assertEqual(response.data['company_name'], serialized_fields['company_name'])
    #         self.assertEqual(response.data['phone_number'], serialized_fields['phone_number'])
    #         self.assertEqual(response.data['mobile_number'], serialized_fields['mobile_number'])
    #         self.assertEqual(response.data['is_signed'], serialized_fields['is_signed'])
    #         self.assertEqual(response.data['salesman'], serialized_fields['salesman'])

    def test_3_manager_create_client(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'first_name': 'new_customer',
            'last_name': 'new_customer',
            'email': 'new_customer@email.com',
            'phone_number': '0000000000',
            'mobile_number': '0000000000',
            'salesman': 2,
            'is_signed': False
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)