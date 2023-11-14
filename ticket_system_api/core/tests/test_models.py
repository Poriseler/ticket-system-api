"""
Tests for models.
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from core.models import Ticket, Comment


class ModelTests(TestCase):
    """Tests for models."""

    def test_create_user_successful(self):
        """Tests if user creation with email as login is successful."""
        email = 'user@example.com'
        password = 'pass123'
        user = get_user_model().objects.create_user(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_create_superuser(self):
        """Tests if superuser creation is successful."""
        email = 'admin@example.com'
        password = 'pass123'
        user = get_user_model().objects.create_superuser(email, password)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))
        self.assertTrue(user.is_superuser)

    def test_normalize_email(self):
        """Tests if email is normalized during user creation."""
        test_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com']
        ]

        password = 'pass123'

        for email, expected_email in test_emails:
            user = get_user_model().objects.create_user(email, password)
            self.assertEqual(user.email, expected_email)

    def test_user_creation_without_password_error(self):
        """Tests if creation user without password raises error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('user@example.com', '')

    def test_user_creation_without_email_error(self):
        """Tests if creation user without email raises error."""

        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'pass123')

    def test_ticket_create(self):
        """Tests if ticket creation is successful."""

        user = get_user_model().objects.create_user('user@example.com', 'pass123')
        user2 = get_user_model().objects.create_user('user2@example.com', 'pass123')
        ticket = Ticket.objects.create(created_by=user, assigned_to=user2,
                                       title='Test title', description='Test description', status='OPEN')

        self.assertEqual(str(ticket), ticket.title)

    def test_comment_create(self):
        """Tests if comment creation is successful."""

        user = get_user_model().objects.create_user('user@example.com', 'pass123')
        user2 = get_user_model().objects.create_user('user2@example.com', 'pass123')
        ticket = Ticket.objects.create(created_by=user, assigned_to=user2,
                                       title='Test title', description='Test description', status='OPEN')

        comment = Comment.objects.create(
            ticket=ticket, author=user, text='Example comment text')

        self.assertEqual(
            str(comment), f'{comment.ticket.id}_{comment.text[:20]}')
