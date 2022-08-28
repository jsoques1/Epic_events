import pytest
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
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

    def check_login(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue("access" in response.data)
        self.assertTrue("refresh" in response.data)

    def test_1_manager_login_ok(self):
        self.check_login('mgr', 'mgr')

    def test_1_sales_login_ok(self):
        self.check_login('sales', 'sales')

    def test_1_support_login_ok(self):
        self.check_login('support', 'support')

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

        self.client.credentials(HTTP_AUTHORIZATION="Bearer 'token'")
        url = reverse("customers-list")
        response = self.client.get(url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @pytest.mark.django_db
    def test_login_user_unknown(self):
        url = reverse("login")
        data = {"username": 'unknown', "password": 'unknown'}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
