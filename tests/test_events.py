import pytest
from django.core.management import call_command
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase
from crm.models import Event, Contract
from users.models import User, MGMT, SALES, SUPPORT
from rest_framework import status
import json
from django.core import serializers


class TestEvent(APITestCase):
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

    def check_events_list(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        url = reverse("events-list")
        response = self.client.get(url, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), len(Event.objects.all()))
        for event in response.data['results']:
            event = dict(event)
            db_event = Event.objects.get(id=event['id'])
            serialized_obj = serializers.serialize('json', [db_event, ])
            res = json.loads(serialized_obj)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(event['id'], res[0]['pk'])
            serialized_fields = res[0]['fields']
            self.assertEqual(event['contract'], serialized_fields['contract'])
            self.assertEqual(event['support'], serialized_fields['support'])
            self.assertEqual(event['name'], serialized_fields['name'])
            self.assertEqual(serialized_fields['event_date'], serialized_fields['event_date'])
            self.assertEqual(event['location'], serialized_fields['location'])
            self.assertEqual(event['attendees'], serialized_fields['attendees'])
            self.assertEqual(event['is_completed'], serialized_fields['is_completed'])

    def check_event_detail(self, username, password):
        url = reverse("login")
        data = {"username": username, "password": password}
        response = self.client.post(url, data, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        for customer_id in range(1, 6):
            url = reverse("events-detail", args=(customer_id,))
            response = self.client.get(url, format="json")
            event = Event.objects.get(id=customer_id)

            serialized_obj = serializers.serialize('json', [event, ])
            res = json.loads(serialized_obj)

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(response.data['id'], res[0]['pk'])
            serialized_fields = res[0]['fields']
            self.assertEqual(response.data['contract'], serialized_fields['contract'])
            self.assertEqual(response.data['support'], serialized_fields['support'])
            self.assertEqual(response.data['name'], serialized_fields['name'])
            self.assertEqual(serialized_fields['event_date'], serialized_fields['event_date'])
            self.assertEqual(response.data['location'], serialized_fields['location'])
            self.assertEqual(response.data['attendees'], serialized_fields['attendees'])
            self.assertEqual(response.data['is_completed'], serialized_fields['is_completed'])

    def check_event_CRUD(self, username, password, crud_status, is_completed):
        url = reverse("login")
        if username == 'support1':
            data_user = {"username": 'sales1', "password": 'sales1'}
        else:
            data_user = {"username": username, "password": password}
        response = self.client.post(url, data_user, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")
        data = {
            'salesman': 2,
            'customer': 1,
            'amount': 1000.0,
            'is_signed': True,
            'company_name': 'test',
            'payment_due': '2023-02-27'
        }
        response = self.client.post('/crm/contracts/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        if username == 'support1':
            data_user = {"username": 'sales1', "password": 'sales1'}
        else:
            data_user = {"username": username, "password": password}
        response = self.client.post(url, data_user, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        data = {
            'contract': 6,
            'name': 'La foire a 1 euro',
            'event_date': '2023-01-10 12:00:00',
            'location': 'Passy',
            'attendees': '10000',
            'notes': 'Pink Champagne only',
            'is_completed': is_completed
        }
        response = self.client.post('/crm/events/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_user = {"username": username, "password": password}
        response = self.client.post(url, data_user, format="json")
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {response.data['access']}")

        if crud_status['U'] and username == 'mgr':
            data = {
                'id': 6,
                'contract': 6,
                'support': 3,
                'name': 'La foire a 2 euros',
                'event_date': '2023-01-10 12:00:00',
                'location': 'Passy',
                'attendees': '10000',
                'notes': 'Pink Champagne only',
                'is_completed': is_completed,
            }
            response = self.client.put('/crm/events/6/', data, format='json')

            self.assertEqual(response.status_code, status.HTTP_200_OK)
        elif crud_status['U'] and username == 'support1':
            data = {
                'id': 6,
                'name': 'La foire a 2 euros',
                'event_date': '2023-01-10 12:00:00',
                'contract': 6,
                'location': 'Passy',
                'attendees': '10000',
                'notes': 'Pink Champagne only',
                'is_completed': is_completed,
            }
            response = self.client.put('/crm/events/6/', data, format='json')
            if is_completed:
                self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = self.client.delete('/crm/events/6/', data, format='json')
        if crud_status['D']:
            if username == 'support1':
                if is_completed:
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                else:
                    self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            else:
                self.assertEqual(response.status_code, status.HTTP_200_OK)
        else:
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_1_manager_get_events_list(self):
        self.check_events_list('mgr', 'mgr')

    def test_1_sales_get_events_list(self):
        self.check_events_list('sales1', 'sales1')

    def test_1_support_get_events_list(self):
        self.check_events_list('support1', 'support1')

    def test_2_manager_get_events_detail(self):
        self.check_event_detail('mgr', 'mgr')

    def test_2_sales_get_events_detail(self):
        self.check_event_detail('sales1', 'sales1')

    def test_2_support_get_events_detail(self):
        self.check_event_detail('support1', 'support1')

    @pytest.mark.django_db()
    def test_3a_manager_event_not_completed_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_event_CRUD('mgr', 'mgr', crud_status, is_completed=False)

    @pytest.mark.django_db()
    def test_3a_manager_event_completed_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': True, 'D': True}
        self.check_event_CRUD('mgr', 'mgr', crud_status, is_completed=True)

    @pytest.mark.django_db()
    def test_3a_sales_event_not_completed_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': False, 'D': False}
        self.check_event_CRUD('sales1', 'sales1', crud_status, is_completed=False)

    @pytest.mark.django_db()
    def test_3a_sales_event_completed_CRUD(self):
        crud_status = {'C': True, 'R': True, 'U': False, 'D': False}
        self.check_event_CRUD('sales1', 'sales1', crud_status, is_completed=True)

    @pytest.mark.django_db()
    def test_3a_support_event_not_completed_CRUD(self):
        crud_status = {'C': False, 'R': True, 'U': True, 'D': True}
        self.check_event_CRUD('support1', 'support1', crud_status, is_completed=False)

    @pytest.mark.django_db()
    def test_3a_support_event_completed_CRUD(self):
        crud_status = {'C': False, 'R': True, 'U': True, 'D': True}
        self.check_event_CRUD('support1', 'support1', crud_status, is_completed=True)
