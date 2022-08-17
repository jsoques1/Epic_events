import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Customer, Contract, Event
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status


class TestCustomer(APITestCase):
    @pytest.mark.django_db
    def setUp(self):

        User.objects.create_user(
            username='mgr',
            password='mgr',
            role=MGMT,
        )

        User.objects.create_user(
            username='sales',
            password='sales',
            role=SALES,
        )

        User.objects.create_user(
            username='support',
            password='support',
            role=SUPPORT,
        )

        call_command('loaddata', 'customers.json', verbosity=0)

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
    def test_manager_get_customers_list(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-list")
        print(url)
        response = self.client.get(url, format="json")
        print(response.data['results'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))

    @pytest.mark.django_db
    def test_manager_get_customer_detail(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("customers-detail", args=(1,))
        print(url)
        response = self.client.get(url, format="json")
        print(response.data['results'])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Customer.objects.all()))