"""
Tests for tickets api.
"""
from datetime import datetime

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Ticket

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from ticket.serializers import TicketSerializer

TICKET_URL = reverse('ticket:ticket-list')

def ticket_details(ticket_url):
    return reverse('ticket:ticket-detail', args=[ticket_url])

def create_user(email='user@example.com', password='pass123'):
    payload = {
        'name': 'User',
        'surname': 'Testowsky'
    }
    return get_user_model().objects.create_user(email, password, **payload)

def create_ticket(created_by, assigned_to, **extra_fields):
    payload = {
        'status': 'OPEN',
        'title': 'Test case',
        'description': 'Everything should work as expected'
    }
    payload.update(**extra_fields)
    return Ticket.objects.create(created_by=created_by, assigned_to=assigned_to, **payload)

class PublicTicketApiTests(TestCase):
    """Tests for unauthenticated API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieving_ticket_list(self):
        """Tests if retrieving list of all tickets is successful."""
        user = create_user()
        user2 = create_user(email='user2@example.com')
        create_ticket(user, user2)
        create_ticket(user2, user)

        tickets = Ticket.objects.all().order_by('-id')
        res = self.client.get(TICKET_URL)
        serializer = TicketSerializer(tickets, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieving_ticket_details(self):
        """Tests if retrieving details of ticket is successful."""
        user = create_user()
        user2 = create_user(email='user2@example.com')
        ticket = create_ticket(user, user2)
        res = self.client.get(ticket_details(ticket.id))

        serializer = TicketSerializer(ticket)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_creating_ticket_forbidden(self):
        """Tests if anonymous users can't create tickets."""
        user = create_user()
        user2 = create_user(email='user2@example.com')
        ts = datetime.now()
        payload = {
            'created_by': user,
            'assigned_to': user2,
            'status': 'OPEN',
            'title': 'Test case',
            'description': 'Everything should work as expected',
            'created_at': ts,
            'updated_at': ts
        }
        res = self.client.post(TICKET_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_deleting_ticket_forbidden(self):
        """Tests if deleting ticket by anonymous user is forbidden."""
        user = create_user()
        user2 = create_user(email='user2@example.com')
        ticket = create_ticket(user, user2)
        res = self.client.delete(ticket_details(ticket.id))

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_modifying_ticket_forbidden(self):
        """Tests if modifying ticket by anonymous user is forbidden."""
        user = create_user()
        user2 = create_user(email='user2@example.com')
        ticket = create_ticket(user, user2)
        payload = {
            'description': 'Changed description',
            'status': 'CLOSED'
        }
        res = self.client.patch(ticket_details(ticket.id), payload)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
