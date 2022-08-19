import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Customer, Contract, Event
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status


class TestLogin(APITestCase):
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

    @pytest.mark.django_db
    def test_manager_login_ok(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    @pytest.mark.django_db
    def test_manager_login_wrong_password(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'unknown'}
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.django_db
    def test_manager_login_wrong_token(self):
        url = reverse("login")
        data = {"username": 'mgr', "password": 'mgr'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer 'token'")
        url = reverse("customers-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.django_db
    def test_login_user_unknown(self):
        url = reverse("login")
        data = {"username": 'unknown', "password": 'unknown'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
