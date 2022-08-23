import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Customer
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status
import json
from django.core import serializers
import time


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

    def check_login(self, username, password):
        data = {"username": username, "password": password}
        response = self.client.post('/login', data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    @pytest.mark.django_db
    def test_login_ok(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)
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

    @pytest.mark.django_db()
    def test_3a_manager_prospect_CRUD(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        print(Customer.objects.filter())

    # @pytest.mark.django_db()
    # def test_3b_manager_get_customers_number(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get('/crm/customers/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
        print(len(response.data['results']))

    # @pytest.mark.django_db()
    # def test_3b_manager_modify_prospect(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': True,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        print(response.data)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, data)
        response = self.client.delete('/crm/customers/6/', data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db()
    def test_3b_manager_client_CRUD(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'first_name': 'prospect',
            'last_name': 'prospect',
            'email': 'prospect@email.com',
            'company_name': 'new_prospect',
            'phone_number': '0000000000',
            'mobile_number': '0000000000',
            'is_signed': True,
            'salesman': 2,
        }
        response = self.client.post('/crm/customers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        print(Customer.objects.filter())

        # @pytest.mark.django_db()
        # def test_3b_manager_get_customers_number(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get('/crm/customers/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
        print(len(response.data['results']))

        # @pytest.mark.django_db()
        # def test_3b_manager_modify_prospect(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': False,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        print(response.data)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, data)
        response = self.client.delete('/crm/customers/6/', data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db()
    def test_4a_sales_prospect_CRUD(self):
        url = reverse("login")
        data = {"username": 'sales1', "password": 'sales1'}
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
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        print(Customer.objects.filter())

    # @pytest.mark.django_db()
    # def test_3b_manager_get_customers_number(self):
        url = reverse("login")
        data = {"username": 'sales1', "password": 'sales1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get('/crm/customers/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
        print(len(response.data['results']))

    # @pytest.mark.django_db()
    # def test_3b_manager_modify_prospect(self):
        url = reverse("login")
        data = {"username": 'sales1', "password": 'sales1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': True,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        print(response.data)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, data)
        response = self.client.delete('/crm/customers/6/', data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db()
    def test_4b_sales_client_CRUD(self):
        url = reverse("login")
        data = {"username": 'sales1', "password": 'sales1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'first_name': 'prospect',
            'last_name': 'prospect',
            'email': 'prospect@email.com',
            'company_name': 'new_prospect',
            'phone_number': '0000000000',
            'mobile_number': '0000000000',
            'is_signed': True,
            'salesman': 2,
        }
        response = self.client.post('/crm/customers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
        print(Customer.objects.filter())

        # @pytest.mark.django_db()
        # def test_3b_manager_get_customers_number(self):
        url = reverse("login")
        data = {"username": 'sales1', "password": 'sales1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get('/crm/customers/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
        print(len(response.data['results']))

        # @pytest.mark.django_db()
        # def test_3b_manager_modify_prospect(self):
        url = reverse("login")
        data = {"username": 'sales1', "password": 'sales1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': False,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        print(response.data)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # self.assertEqual(response.data, data)
        response = self.client.delete('/crm/customers/6/', data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @pytest.mark.django_db()
    def test_5a_support_prospect_CRUD(self):
        url = reverse("login")
        data = {"username": 'support1', "password": 'support1'}
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
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(Customer.objects.filter())

    # @pytest.mark.django_db()
    # def test_3b_manager_get_customers_number(self):
        url = reverse("login")
        data = {"username": 'support1', "password": 'support1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get('/crm/customers/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
        print(len(response.data['results']))

    # @pytest.mark.django_db()
    # def test_3b_manager_modify_prospect(self):
        url = reverse("login")
        data = {"username": 'support1', "password": 'support1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': True,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        print(response.data)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data, data)
        response = self.client.delete('/crm/customers/6/', data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @pytest.mark.django_db()
    def test_5b_support_client_CRUD(self):
        url = reverse("login")
        data = {"username": 'support1', "password": 'support1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'first_name': 'prospect',
            'last_name': 'prospect',
            'email': 'prospect@email.com',
            'company_name': 'new_prospect',
            'phone_number': '0000000000',
            'mobile_number': '0000000000',
            'is_signed': True,
            'salesman': 2,
        }
        response = self.client.post('/crm/customers/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        print(Customer.objects.filter())

        # @pytest.mark.django_db()
        # def test_3b_manager_get_customers_number(self):
        url = reverse("login")
        data = {"username": 'support1', "password": 'support1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        response = self.client.get('/crm/customers/', format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))
        print(len(response.data['results']))

        # @pytest.mark.django_db()
        # def test_3b_manager_modify_prospect(self):
        url = reverse("login")
        data = {"username": 'support1', "password": 'support1'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'id': 6,
            'first_name': 'modified_prospect',
            'last_name': 'modified_prospect',
            'email': 'modified_prospect@email.com',
            'company_name': 'modified_prospect',
            'phone_number': '111111111',
            'mobile_number': '111111111',
            'is_signed': False,
            'salesman': 2
        }
        response = self.client.put('/crm/customers/6/', data, format='json')
        print(response.data)
        print(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        # self.assertEqual(response.data, data)
        response = self.client.delete('/crm/customers/6/', data, format='json')

        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
