"""
Views for Ticket API.
"""

from ticket import serializers

from core.models import User, Ticket, Comment
from core.custom_permissions import IsOwnerOrAdminOrReadOnly

from rest_framework import viewsets, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response


class TicketViewSet(viewsets.ModelViewSet):
    """View for managing ticket API."""
    serializer_class = serializers.TicketSerializer
    queryset = Ticket.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        """Creates a new ticket."""
        serializer.save(created_by=self.request.user)

    def get_queryset(self):
        """Gets queryset basing on query params if provided."""
        queryset = self.queryset
        assigned_user_id = self.request.query_params.get('assigned')
        createor_id = self.request.query_params.get('creator')
        order_by = self.request.query_params.get(
            'order-by')

        if assigned_user_id:
            queryset = queryset.filter(
                assigned_to__id__exact=assigned_user_id).order_by('-id')
        if createor_id:
            queryset = queryset.filter(
                created_by__id__exact=createor_id
            ).order_by('-id')
        if order_by:
            order_by, direction = order_by.split('-')
            if direction == 'Asc':
                queryset = queryset.order_by(order_by)
            elif direction == 'Desc':
                queryset = queryset.order_by(f'-{order_by}')
        return queryset


class CommentViewSet(viewsets.ModelViewSet):
    """View for managing comments API."""
    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        """Created a new comment."""
        serializer.save(author=self.request.user)
