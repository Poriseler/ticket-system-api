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
from ticket.serializers import TicketSerializer, TicketDetailSerializer

TICKET_URL = reverse('ticket:ticket-list')


def ticket_details(ticket_url):
    return reverse('ticket:ticket-detail', args=[ticket_url])


def create_user(email='user@example.com', password='pass123', is_superuser=False):
    payload = {
        'name': 'User',
        'surname': 'Testowsky'
    }
    if is_superuser:
        return get_user_model().objects.create_superuser(email, password, **payload)

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
        self.assertEqual(res.data.get('results'), serializer.data)

    def test_retrieving_ticket_details(self):
        """Tests if retrieving details of ticket is successful."""

        user = create_user()
        user2 = create_user(email='user2@example.com')
        ticket = create_ticket(user, user2)
        res = self.client.get(ticket_details(ticket.id))
        serializer = TicketDetailSerializer(ticket)

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

    def test_order_by_priority_asc(self):
        """Tests if tickets are ordered by priority ascending."""
        user = create_user()
        user2 = create_user(email='user2@example.com')

        ticket1_options = {'priority': 'MODERATE'}
        ticket2_options = {'status': 'IN_PROGRESS'}
        ticket3_options = {'priority': 'URGENT'}

        ticket1 = create_ticket(user, user2, **ticket1_options)
        ticket2 = create_ticket(user, user2, **ticket2_options)
        ticket3 = create_ticket(user, user2, **ticket3_options)

        res = self.client.get(f'{TICKET_URL}?order-by=priority-asc')
        tickets = Ticket.objects.all().order_by('priority')
        serializer = TicketSerializer(tickets, many=True)

        self.assertEqual(res.data.get('results'), serializer.data)

    def test_order_by_created_at_desc(self):
        """Tests if tickets are ordered by create date descending"""
        user = create_user()
        user2 = create_user(email='user2@example.com')

        ticket1_options = {'priority': 'MODERATE'}
        ticket2_options = {'status': 'IN_PROGRESS'}
        ticket3_options = {'priority': 'URGENT'}

        ticket1 = create_ticket(user, user2, **ticket1_options)
        ticket2 = create_ticket(user, user2, **ticket2_options)
        ticket3 = create_ticket(user, user2, **ticket3_options)

        res = self.client.get(f'{TICKET_URL}?order-by=created_at-desc')
        tickets = Ticket.objects.all().order_by('-created_at')
        serializer = TicketSerializer(tickets, many=True)

        self.assertEqual(res.data.get('results'), serializer.data)

    def test_order_by_updated_at_asc(self):
        """Tests if tickets are ordered by update date ascending."""

        user = create_user()
        user2 = create_user(email='user2@example.com')

        ticket1_options = {'priority': 'MODERATE'}
        ticket2_options = {'status': 'IN_PROGRESS'}
        ticket3_options = {'priority': 'URGENT'}

        ticket1 = create_ticket(user, user2, **ticket1_options)
        ticket2 = create_ticket(user, user2, **ticket2_options)
        ticket3 = create_ticket(user, user2, **ticket3_options)

        res = self.client.get(f'{TICKET_URL}?order-by=updated_at-asc')
        tickets = Ticket.objects.all().order_by('updated_at')
        serializer = TicketSerializer(tickets, many=True)

        self.assertEqual(res.data.get('results'), serializer.data)

    def test_order_by_status_desc(self):
        """Tests if tickets are ordered by status descending."""

        user = create_user()
        user2 = create_user(email='user2@example.com')

        ticket1_options = {'priority': 'MODERATE'}
        ticket2_options = {'status': 'IN_PROGRESS'}
        ticket3_options = {'priority': 'URGENT'}

        ticket1 = create_ticket(user, user2, **ticket1_options)
        ticket2 = create_ticket(user, user2, **ticket2_options)
        ticket3 = create_ticket(user, user2, **ticket3_options)

        res = self.client.get(f'{TICKET_URL}?order-by=status-desc')
        tickets = Ticket.objects.all().order_by('-status')
        serializer = TicketSerializer(tickets, many=True)

        self.assertEqual(res.data.get('results'), serializer.data)


class PrivateTicketApiTests(TestCase):
    """Tests for requests from authorized users."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieving_tickets_for_user(self):
        """Tests if only tickets for specified user are returned."""

        user2 = create_user(email='user2@example.com')
        user3 = create_user(email='user3@example.com')

        ticket1 = create_ticket(
            created_by=user2,
            assigned_to=self.user
        )
        ticket2 = create_ticket(
            created_by=user2,
            assigned_to=user3
        )
        ticket3 = create_ticket(
            created_by=user3,
            assigned_to=self.user
        )

        res = self.client.get(TICKET_URL, {'assigned': self.user.id})

        serialized_ticket1 = TicketSerializer(ticket1)
        serialized_ticket2 = TicketSerializer(ticket2)
        serialized_ticket3 = TicketSerializer(ticket3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serialized_ticket1.data, res.data.get('results'))
        self.assertNotIn(serialized_ticket2.data, res.data.get('results'))
        self.assertIn(serialized_ticket3.data, res.data.get('results'))

    def test_retrieving_tickets_created_by_user(self):
        """Tests if only tickets created by user are returned."""

        user2 = create_user(email='user2@example.com')
        user3 = create_user(email='user3@example.com')

        ticket1 = create_ticket(
            created_by=self.user,
            assigned_to=user2
        )
        ticket2 = create_ticket(
            created_by=user2,
            assigned_to=user3
        )
        ticket3 = create_ticket(
            created_by=self.user,
            assigned_to=user2
        )

        res = self.client.get(TICKET_URL, {'creator': self.user.id})

        serialized_ticket1 = TicketSerializer(ticket1)
        serialized_ticket2 = TicketSerializer(ticket2)
        serialized_ticket3 = TicketSerializer(ticket3)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn(serialized_ticket1.data, res.data.get('results'))
        self.assertNotIn(serialized_ticket2.data, res.data.get('results'))
        self.assertIn(serialized_ticket3.data, res.data.get('results'))

    def test_deleting_ticket_by_creator(self):
        """Tests if ticket can be deleted by it's creator. """

        user2 = create_user(email='user2@example.com')
        ticket = create_ticket(
            created_by=self.user,
            assigned_to=user2
        )
        url = ticket_details(ticket.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tickets = Ticket.objects.all()
        self.assertEqual(tickets.count(), 0)

    def test_deleting_ticket_by_superuser(self):
        """Tests if ticket can be deleted by superuser. """

        user2 = create_user(email='user2@example.com')
        superuser = create_user('admin@example.com', 'testpass123', True)
        self.client.force_authenticate(superuser)

        ticket = create_ticket(
            created_by=self.user,
            assigned_to=user2
        )

        url = ticket_details(ticket.id)
        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        tickets = Ticket.objects.all()
        self.assertEqual(tickets.count(), 0)

    def test_modyfing_ticket_by_creator(self):
        """Tests if ticket can be modified by it's creator. """

        user2 = create_user(email='user2@example.com')

        ticket = create_ticket(
            created_by=self.user,
            assigned_to=user2
        )
        payload = {
            'description': 'Modified description'
        }

        url = ticket_details(ticket.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_modyfing_ticket_by_superuser(self):
        """Tests if ticket can be modified by superuser. """

        user2 = create_user(email='user2@example.com')
        superuser = create_user('admin@example.com', 'testpass123', True)
        self.client.force_authenticate(superuser)

        ticket = create_ticket(
            created_by=self.user,
            assigned_to=user2
        )
        payload = {
            'description': 'Modified description'
        }

        url = ticket_details(ticket.id)

        res = self.client.patch(url, payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_creating_ticket(self):
        """Tests successful creation of ticket by authenticated user."""

        user2 = create_user(email='user2@example.com')
        payload = {
            'title': "Example title",
            'description': 'Example desciption',
            'priority': 'URGENT',
            'assigned_to': user2.pk
        }

        res = self.client.post(TICKET_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

        for k, v in payload.items():
            self.assertEqual(res.data.get(k), v)
