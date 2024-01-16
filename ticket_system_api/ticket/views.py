"""
Views for Ticket API.
"""

from ticket import serializers

import math

from user.serializers import UserArticleSerializer

from core.models import User, Ticket, Comment
from core.custom_permissions import IsOwnerOrAdminOrReadOnly
from django.contrib.auth import get_user_model

from rest_framework import viewsets, status, generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination


class TicketViewSet(viewsets.ModelViewSet):
    """View for managing ticket API."""

    serializer_class = serializers.TicketSerializer
    queryset = Ticket.objects.all().order_by('-id')
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination

    def perform_create(self, serializer):
        """Creates a new ticket."""

        serializer.save(created_by=self.request.user)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.TicketDetailSerializer
        if self.action == 'list':
            return serializers.TicketSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        """Gets queryset basing on query params if provided."""

        queryset = self.queryset
        assigned_user_id = self.request.query_params.get('assigned')
        createor_id = self.request.query_params.get('creator')
        order_by = self.request.query_params.get(
            'order-by')
        ticket_id = self.request.query_params.get('ticket-id')
        ticket_title = self.request.query_params.get('ticket-title')

        if assigned_user_id:
            queryset = queryset.filter(
                assigned_to__id__exact=assigned_user_id).order_by('-id')
        if createor_id:
            queryset = queryset.filter(
                created_by__id__exact=createor_id
            ).order_by('-id')
        if ticket_id:
            queryset = queryset.filter(
                id__exact=ticket_id
            )
        if ticket_title:
            queryset = queryset.filter(
                title__icontains=ticket_title
            )

        if order_by:
            order_by, direction = order_by.split('-')
            if direction == 'asc':
                queryset = queryset.order_by(order_by)
            elif direction == 'desc':
                queryset = queryset.order_by(f'-{order_by}')

        return queryset

    @action(methods=['GET'], detail=False, url_path='assigned-to-me')
    def get_tickets_assigned_to_me(self, request):
        """Get tickets assigned to user that sent request."""

        if not request.user:
            return Response('User not logged in', status=status.HTTP_400_BAD_REQUEST)

        queryset = Ticket.objects.filter(assigned_to__exact=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.TicketSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(methods=['GET'], detail=False, url_path='my-tickets')
    def get_tickets_created_by_me(self, request):
        """Get tickets created by user that sent request."""

        if not request.user:
            return Response('User not logged in', status=status.HTTP_400_BAD_REQUEST)

        queryset = Ticket.objects.filter(created_by__exact=request.user)
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = serializers.TicketSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = serializers.TicketSerializer(queryset, many=True)
        return Response(serializer.data)


class CommentViewSet(viewsets.ModelViewSet):
    """View for managing comments API."""

    serializer_class = serializers.CommentSerializer
    queryset = Comment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrAdminOrReadOnly]

    def perform_create(self, serializer):
        """Created a new comment."""
        serializer.save(author=self.request.user)


class MetricView(generics.GenericAPIView):
    """View for returning metrics."""

    def get(self, request, *args, **kwargs):
        total_tickets = Ticket.objects.all()
        tickets_open = Ticket.objects.filter(status='OPEN')
        tickets_closed = Ticket.objects.filter(status='CLOSED')
        tickets_in_progress = Ticket.objects.filter(status='IN_PROGRESS')
        total_closing_time = 0
        for ticket in tickets_closed:
            total_closing_time += (ticket.updated_at -
                                   ticket.created_at).total_seconds()
        try:
            avg_ticket_closing_time = total_closing_time/len(tickets_closed)
        except ZeroDivisionError:
            avg_ticket_closing_time = 0

        data = {
            'total_tickets': len(total_tickets),
            'tickets_open': len(tickets_open),
            'tickets_in_progress': len(tickets_in_progress),
            'tickets_closed': len(tickets_closed),
            'avg_closing_time_mins': math.floor(avg_ticket_closing_time/60)

        }
        return Response(data)


class EmployeesView(generics.GenericAPIView):
    """View for returning employees from system."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        queryset = get_user_model().objects.filter(
            is_staff=True).exclude(id=request.user.id)
        serializer = UserArticleSerializer(queryset, many=True)

        return Response(serializer.data)
