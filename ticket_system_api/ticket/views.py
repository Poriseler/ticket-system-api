"""
Views for Ticket API.
"""

from ticket import serializers

from core.models import User, Ticket

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

class TicketViewSet(viewsets.ModelViewSet):
    """View for managing ticket API."""
    serializer_class = serializers.TicketSerializer
    queryset = Ticket.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)

