import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Contract
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status
import json
from django.core import serializers
import time


class TestContract(APITestCase):
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

    def check_contracts_list(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("contracts-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Contract.objects.all()))
        for contract in response.data['results']:
            contract = dict(contract)
            db_contract = Contract.objects.get(id=contract['id'])
            serialized_obj = serializers.serialize('json', [db_contract, ])
            res = json.loads(serialized_obj)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(contract['id'], res[0]['pk'])
            serialized_fields = res[0]['fields']
            self.assertEqual(contract['salesman'], serialized_fields['salesman'])
            self.assertEqual(contract['customer'], serialized_fields['customer'])
            self.assertEqual(contract['is_signed'], serialized_fields['is_signed'])
            self.assertEqual(contract['amount'], serialized_fields['amount'])
            self.assertEqual(contract['payment_due'], serialized_fields['payment_due'])

    def check_contract_detail(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        for customer_id in range(1, 6):
            url = reverse("contracts-detail", args=(customer_id,))
            response = self.client.get(url, format="json")
            contract = Contract.objects.get(id=customer_id)

            serialized_obj = serializers.serialize('json', [contract, ])
            res = json.loads(serialized_obj)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['id'], res[0]['pk'])
            serialized_fields = res[0]['fields']
            self.assertEqual(response.data['salesman'], serialized_fields['salesman'])
            self.assertEqual(response.data['customer'], serialized_fields['customer'])
            self.assertEqual(response.data['is_signed'], serialized_fields['is_signed'])
            self.assertEqual(response.data['amount'], serialized_fields['amount'])
            self.assertEqual(response.data['payment_due'], serialized_fields['payment_due'])

    def check_contract_CRUD(self, username, password, crud_status, is_signed):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'salesman': 2,
            'customer': 1,
            'amount': 1000.0,
            'is_signed': is_signed,
            'company_name': 'new_prospect',
            'payment_due': '2023-02-27'
        }
        response = self.client.post('/crm/contracts/', data, format='json')
        if crud_status['C']:
            self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.get('/crm/contracts/', format="json")
        # if crud_status['R']:
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Contract.objects.all()))

        data = {
            'id': 6,
            'salesman': 2,
            'customer': 1,
            'amount': 1000.0,
            'is_signed': is_signed,
            'company_name': 'new_prospect',
            'payment_due': '2023-02-27'
        }
        response = self.client.put('/crm/contracts/6/', data, format='json')
        if crud_status['U']:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        response = self.client.delete('/crm/contracts/6/', data, format='json')
        if crud_status['D']:
            self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_1_manager_get_contracts_list(self):
        self.check_contracts_list('mgr', 'mgr')

    def test_1_sales_get_contracts_list(self):
        self.check_contracts_list('sales1', 'sales1')

    def test_1_support_get_contracts_list(self):
        self.check_contracts_list('support1', 'support1')

    def test_2_manager_get_customer_detail(self):
        self.check_contract_detail('mgr', 'mgr')

    def test_2_sales_get_customer_detail(self):
        self.check_contract_detail('sales1', 'sales1')

    def test_3_support_get_customer_detail(self):
        self.check_contract_detail('support1', 'support1')

    @pytest.mark.django_db()
    def test_3a_manager_prospect_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_contract_CRUD('mgr', 'mgr', crud_status, is_signed=False)

    @pytest.mark.django_db()
    def test_3b_manager_customer_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_contract_CRUD('mgr', 'mgr', crud_status, is_signed=True)

    @pytest.mark.django_db()
    def test_3a_sales_prospect_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_contract_CRUD('sales1', 'sales1', crud_status, is_signed=False)

    @pytest.mark.django_db()
    def test_3b_sales_customer_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_contract_CRUD('sales1', 'sales1', crud_status, is_signed=True)

    @pytest.mark.django_db()
    def test_3a_support_prospect_CRUD(self):
        crud_status = {'C': False, 'R': True, 'U': False, 'D': False}
        self.check_contract_CRUD('support1', 'support1', crud_status, is_signed=False)

    @pytest.mark.django_db()
    def test_3b_support_customer_CRUD(self):
        crud_status = {'C': False, 'R': True, 'U': False, 'D': False}
        self.check_contract_CRUD('support1', 'support1', crud_status, is_signed=True)
