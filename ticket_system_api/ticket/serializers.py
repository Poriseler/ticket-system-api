"""
Serializers for ticket API.
"""

from core.models import Ticket, Comment
from rest_framework import serializers
from user.serializers import UserArticleSerializer


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for Comment object."""

    ticket = serializers.PrimaryKeyRelatedField(queryset=Ticket.objects.all())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']


class CommentDetailedSerializer(CommentSerializer):
    """Extended serializer for more details."""
    author = UserArticleSerializer()


class TicketSerializer(serializers.ModelSerializer):
    """Serializer for Ticket object."""

    class Meta:
        model = Ticket
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'created_by']


class TicketDetailSerializer(serializers.ModelSerializer):
    """Serializer for Ticket details endpoint."""
    created_by = UserArticleSerializer()
    assigned_to = UserArticleSerializer()
    comments = CommentDetailedSerializer(many=True)

    class Meta:
        model = Ticket
        fields = ['id', 'created_by', 'assigned_to', 'status',
                  'title',
                  'description',
                  'created_at',
                  'updated_at',
                  'priority',
                  'comments']
