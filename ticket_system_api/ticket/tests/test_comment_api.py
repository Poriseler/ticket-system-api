"""Tests for Comment api."""

from rest_framework import status
from rest_framework.test import APIClient

from core.models import Comment, Ticket

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from ticket.serializers import CommentSerializer

COMMENT_URL = reverse('ticket:comment-list')


def create_user(email='user@example.com', password='pass123'):
    payload = {
        'name': 'User',
        'surname': 'Testowsky'
    }
    return get_user_model().objects.create_user(email, password, **payload)


def detail_url(comment_id):
    return reverse('ticket:comment-detail', args=[comment_id])


def create_ticket(created_by, assigned_to, **extra_fields):
    payload = {
        'status': 'OPEN',
        'title': 'Test case',
        'description': 'Everything should work as expected'
    }
    payload.update(**extra_fields)
    return Ticket.objects.create(created_by=created_by, assigned_to=assigned_to, **payload)


def create_comment(author, ticket, text='Example comment text.'):
    return Comment.objects.create(author=author, ticket=ticket, text=text)


class PublicCommentApiTests(TestCase):
    """Tests for unauthenticated requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.user2 = create_user('user2@example.com')
        self.ticket = create_ticket(
            created_by=self.user, assigned_to=self.user2)

    def test_listing_all_comments(self):
        """Tests if listing all comments is successful."""

        comment = create_comment(self.user, self.ticket)
        serializer = CommentSerializer(comment)
        res = self.client.get(COMMENT_URL)

        self.assertIn(serializer.data, res.data.get('results'))
        self.assertEqual(len(res.data.get('results')), 1)

    def test_create_comment_not_allowed(self):
        """Tests if creating comments is not allowed for unauthenticated users."""

        payload = {
            'author': self.user,
            'ticket': self.ticket,
            'text': 'Example comment text.'
        }
        res = self.client.post(COMMENT_URL, payload)

        self.assertEqual(res.status_code, 401)

    def test_delete_comment_not_allowed(self):
        """Tests if deleting comments is not allowed for unauthenticated users."""

        comment = create_comment(self.user, self.ticket)
        res = self.client.delete(detail_url(comment.id))

        self.assertEqual(res.status_code, 401)

    def test_edit_comment_not_allowed(self):
        """Tests if editing comments is not allowed for unauthenticated users."""

        comment = create_comment(self.user, self.ticket)
        payload = {
            'text': 'Changed example text.'
        }
        res = self.client.patch(detail_url(comment.id), payload)

        self.assertEqual(res.status_code, 401)


class PrivateCommmentApiTests(TestCase):
    """Tests for authorized requests."""

    def setUp(self):
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)
        self.user2 = create_user('user2@example.com')
        self.ticket = create_ticket(
            created_by=self.user, assigned_to=self.user2)

    def test_creating_comment_successful(self):
        """Tests if creating a comment is successful."""

        payload = {
            'ticket': self.ticket.id,
            'text': 'Example comment text.'
        }
        res = self.client.post(COMMENT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        comments = Comment.objects.filter(author__id__exact=self.user.id)
        self.assertEqual(comments.count(), 1)

    def test_updating_comment_success(self):
        """Tests if user can successfully update a comment."""

        comment = create_comment(self.user, self.ticket)
        payload = {
            'text': 'Changed comment text.'
        }
        res = self.client.patch(detail_url(comment.id), payload)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertEqual(comment.text, payload['text'])

    def test_deleting_comment_success(self):
        """Tests if user can succesfully delete a comment."""

        comment = create_comment(self.user, self.ticket)
        res = self.client.delete(detail_url(comment.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        comments = Comment.objects.all()
        self.assertEqual(comments.count(), 0)

    def test_updating_different_user_comment_error(self):
        """Tests if updating different user comment is forbidden."""

        comment = create_comment(self.user2, self.ticket)
        payload = {
            'text': 'Comment text changed.'
        }
        res = self.client.patch(detail_url(comment.id), payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_deleting_different_user_comment_error(self):
        """Tests if deleting different user comment is forbidden."""
        comment = create_comment(self.user2, self.ticket)
        res = self.client.delete(detail_url(comment.id))

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
