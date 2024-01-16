"""Tests for employees API."""

from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase

EMPLOYEES_URL = reverse('ticket:employees')


def create_user(email='user@example.com', password='pass123', is_superuser=False):
    payload = {
        'name': 'User',
        'surname': 'Testowsky',
        'is_staff': True
    }
    if is_superuser:
        return get_user_model().objects.create_superuser(email, password, **payload)

    return get_user_model().objects.create_user(email, password, **payload)


class PublicUserApiTests(TestCase):
    """Tests for non-authenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieve_users_forbidden(self):
        """Tests if anonynomus user can't retrieve list of employees."""

        res = self.client.get(EMPLOYEES_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserApiTests(TestCase):
    """Tests for authenticated API requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user(is_superuser=True)
        self.client.force_authenticate(self.user)

    def test_retrieve_employees_success(self):
        """Tests retrieving list of employees."""

        user2 = create_user(email='user2@example.com')
        res = self.client.get(EMPLOYEES_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
