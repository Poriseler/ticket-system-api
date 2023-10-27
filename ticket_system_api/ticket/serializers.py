"""
Serializers for ticket API.
"""

from core.models import Ticket
from rest_framework import serializers

class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket object."""

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']