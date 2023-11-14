"""
Serializers for ticket API.
"""

from core.models import Ticket, Comment
from rest_framework import serializers


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment object."""

    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket object."""

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']
