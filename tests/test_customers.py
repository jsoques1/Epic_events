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
    @pytest.mark.django_db()
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

    def check_customers_list(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))

        for customer in response.data['results']:
            customer = dict(customer)
            db_customer = Customer.objects.get(id=customer['id'])
            serialized_obj = serializers.serialize('json', [db_customer, ])
            res = json.loads(serialized_obj)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(customer['id'], res[0]['pk'])
            serialized_fields = res[0]['fields']
            self.assertEqual(customer['first_name'], serialized_fields['first_name'])
            self.assertEqual(customer['last_name'], serialized_fields['last_name'])
            self.assertEqual(customer['email'], serialized_fields['email'])
            self.assertEqual(customer['company_name'], serialized_fields['company_name'])
            self.assertEqual(customer['phone_number'], serialized_fields['phone_number'])
            self.assertEqual(customer['mobile_number'], serialized_fields['mobile_number'])
            self.assertEqual(customer['is_signed'], serialized_fields['is_signed'])
            self.assertEqual(customer['salesman'], serialized_fields['salesman'])

    def check_customer_detail(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        for customer_id in range(1, 6):
            url = reverse("customers-detail", args=(customer_id,))
            response = self.client.get(url, format="json")
            customer = Customer.objects.get(id=customer_id)

            serialized_obj = serializers.serialize('json', [customer, ])
            res = json.loads(serialized_obj)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['id'], res[0]['pk'])
            serialized_fields = res[0]['fields']
            self.assertEqual(response.data['first_name'], serialized_fields['first_name'])
            self.assertEqual(response.data['last_name'], serialized_fields['last_name'])
            self.assertEqual(response.data['email'], serialized_fields['email'])
            self.assertEqual(response.data['company_name'], serialized_fields['company_name'])
            self.assertEqual(response.data['phone_number'], serialized_fields['phone_number'])
            self.assertEqual(response.data['mobile_number'], serialized_fields['mobile_number'])
            self.assertEqual(response.data['is_signed'], serialized_fields['is_signed'])
            self.assertEqual(response.data['salesman'], serialized_fields['salesman'])

    def check_customer_CRUD(self, username, password, crud_status, is_signed):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'first_name': 'prospect',
            'last_name': 'prospect',
            'email': 'prospect@email.com',
            'company_name': 'new_prospect',
            'phone_number': '0000000000',
            'mobile_number': '0000000000',
            'is_signed': False,
            'salesman': 2,
        }
        response = self.client.post('/crm/customers/', data, format='json')
        if crud_status['C']:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
            self.assertEqual(response.data, data)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get('/crm/customers/', format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))

        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': is_signed,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        if crud_status['U']:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete('/crm/customers/6/', data, format='json')
        if crud_status['D']:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_1_manager_get_customers_list(self):
        self.check_customers_list('mgr', 'mgr')

    def test_1_sales_get_customers_list(self):
        self.check_customers_list('sales1', 'sales1')

    def test_1_support_get_customers_list(self):
        self.check_customers_list('support1', 'support1')

    def test_2_manager_get_customer_detail(self):
        self.check_customer_detail('mgr', 'mgr')

    def test_2_sales_get_customer_detail(self):
        self.check_customer_detail('sales1', 'sales1')

    def test_3_support_get_customer_detail(self):
        self.check_customer_detail('support1', 'support1')

    @pytest.mark.django_db()
    def test_3a_manager_prospect_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_customer_CRUD('mgr', 'mgr', crud_status, is_signed=False)

    @pytest.mark.django_db()
    def test_3b_manager_customer_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_customer_CRUD('mgr', 'mgr', crud_status, is_signed=True)

    @pytest.mark.django_db()
    def test_3a_sales_prospect_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_customer_CRUD('sales1', 'sales1', crud_status, is_signed=False)

    @pytest.mark.django_db()
    def test_3b_sales_customer_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_customer_CRUD('sales1', 'sales1', crud_status, is_signed=True)

    @pytest.mark.django_db()
    def test_3a_support_prospect_CRUD(self):
        crud_status = {'C': False, 'R': True, 'U': False, 'D': False}
        self.check_customer_CRUD('support1', 'support1', crud_status, is_signed=False)

    @pytest.mark.django_db()
    def test_3b_support_customer_CRUD(self):
        crud_status = {'C': False, 'R': True, 'U': False, 'D': False}
        self.check_customer_CRUD('support1', 'support1', crud_status, is_signed=True)
