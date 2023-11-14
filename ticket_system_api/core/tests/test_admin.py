"""
Tests for admin page.
"""
from django.urls import reverse
from django.test import TestCase
from django.contrib.auth import get_user_model
from django.test import Client
from rest_framework import status
from core import models


def generate_admin_listing_url(model_name):
    return reverse(f'admin:core_{ model_name.lower()}_changelist')


def generate_admin_add_url(model_name):
    return reverse(f'admin:core_{model_name.lower()}_add')


def generate_admin_edit_url(model_name, instance_id):
    return reverse(f'admin:core_{model_name.lower()}_change', args=[instance_id])


def create_ticket(created_by, assigned_to):
    payload = {
        'status': 'OPEN',
        'title': 'Test case',
        'description': 'Everything should work as expected'
    }
    return models.Ticket.objects.create(created_by=created_by, assigned_to=assigned_to, **payload)


def create_comment(ticket, author):
    comment_text = 'Lorem ipsum doloret'

    return models.Comment.objects.create(author=author, ticket=ticket, text=comment_text)


class AdminPageTests(TestCase):
    """Tests for admin page."""

    def setUp(self):
        self.client = Client()
        self.superuser = get_user_model().objects.create_superuser(
            email='admin@example.com',
            password='pass123',
            name='Test',
            surname='Adminowsky'
        )
        self.client.force_login(self.superuser)
        self.user = get_user_model().objects.create_user(
            email='user@example.com',
            password='pass123',
            name='User',
            surname='Testowsky')

    def test_user_create_page(self):
        """Tests if user creation page is opening correctly."""
        res = self.client.get(generate_admin_add_url('User'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_edit_page(self):
        """Tests if user edit page is opening correctly."""
        res = self.client.get(generate_admin_edit_url('User', self.user.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_list_page(self):
        """Tests if listing users works correctly."""
        res = self.client.get(generate_admin_listing_url('User'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, self.superuser.email)
        self.assertContains(res, self.user.email)

    def test_ticket_create_page(self):
        """Tests if ticket creation page is opening correctly."""
        res = self.client.get(generate_admin_add_url('Ticket'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ticket_edit_page(self):
        """Tests if ticket edit page is opening correctly."""
        ticket = create_ticket(self.superuser, self.user)
        res = self.client.get(generate_admin_edit_url('Ticket', ticket.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_ticket_list_page(self):
        """Tests if listing tickets works correctly."""
        ticket = create_ticket(self.superuser, self.user)
        res = self.client.get(generate_admin_listing_url('Ticket'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, ticket.title)

    def test_comment_create_page(self):
        """Tests if comment creation page is opening correctly."""
        res = self.client.get(generate_admin_add_url('Comment'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_comment_edit_page(self):
        """Tests if comment edit page is opening correctly."""
        ticket = create_ticket(self.superuser, self.user)
        comment = create_comment(ticket, self.user)
        res = self.client.get(generate_admin_edit_url('Comment', comment.id))

        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_comment_list_page(self):
        """Tests if listing comments works correctly."""
        ticket = create_ticket(self.superuser, self.user)
        comment = create_comment(ticket, self.user)
        res = self.client.get(generate_admin_listing_url('Comment'))

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertContains(res, comment)
