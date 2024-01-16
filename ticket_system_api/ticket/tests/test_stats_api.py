"""
Tests for stats API.
"""
from rest_framework import status
from rest_framework.test import APIClient

from django.urls import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from ticket.serializers import TicketSerializer, TicketDetailSerializer

STATS_URL = reverse('ticket:metrics')


class PublicStatsApiTests(TestCase):
    """Tests for unauthorized API requests."""

    def setUp(self):
        self.client = APIClient()

    def test_retrieving_stats(self):
        """Tests if retrieving stats is successful."""

        res = self.client.get(STATS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
