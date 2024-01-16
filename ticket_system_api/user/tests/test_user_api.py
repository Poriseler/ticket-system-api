"""
Tests for user API.
"""
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from ticket.serializers import TicketSerializer, TicketDetailSerializer

PROFILE_URL = reverse('user:me')
TOKEN_URL = reverse('user:token')
USER_CREATE_URL = reverse('user:create')


def create_user(email='user@example.com', password='pass123', is_superuser=False):
    payload = {
        'name': 'User',
        'surname': 'Testowsky'
    }
    if is_superuser:
        return get_user_model().objects.create_superuser(email, password, **payload)

    return get_user_model().objects.create_user(email, password, **payload)


class PublicUserApiTests(TestCase):
    """Tests for non-authenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieving_token(self):
        "Tests if token is returned when loggin in."

        self.user = create_user()
        payload = {
            'email': 'user@example.com',
            'password': 'pass123'
        }

        res = self.client.post(TOKEN_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_creating_user_by_anonymous_user(self):
        """Tests creating users by anonymous user."""
        payload = {
            'email': 'CreatedUser@example.com',
            'password': 'testpass123',
            'name': 'CreatedName',
            'surname': 'CreatedSurname',
        }
        client = APIClient()
        res = client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests for authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_retrieving_profile_data(self):
        """Tests if data from profile is returned"""

        res = self.client.get(PROFILE_URL)
        profile_data = [self.user.email, self.user.name, self.user.surname]

        self.assertEqual(res.status_code, status.HTTP_200_OK)

        for val in res.data.values():
            self.assertIn(val, profile_data)

    def test_modifying_profile_data(self):
        payload = {
            'name': 'ChangedName',
            'surname': "ChangedSurname",
        }

        res = self.client.patch(PROFILE_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.user.name, payload.get('name'))
        self.assertEqual(self.user.surname, payload.get('surname'))

    def test_creating_user_by_superuser(self):
        """Tests if superuser can create another user."""
        payload = {
            'email': 'CreatedUser@example.com',
            'password': 'testpass123',
            'name': 'CreatedName',
            'surname': 'CreatedSurname',
        }
        res = self.client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for k, v in res.data.items():
            self.assertEqual(payload.get(k), v)

    def test_creating_user_by_normal_user(self):
        """Tests creating users by regular user."""
        payload = {
            'email': 'CreatedUser@example.com',
            'password': 'testpass123',
            'name': 'CreatedName',
            'surname': 'CreatedSurname',
        }
        client = APIClient()
        regular_user = create_user(email='regular_user@example.com')
        client.force_authenticate(regular_user)
        res = client.post(USER_CREATE_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
