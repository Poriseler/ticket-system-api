"""
Database models.
"""

from django.db import models
from django.utils import timezone

from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from ticket_system_api import settings


class UserManager(BaseUserManager):
    """Manager for users."""

    def create_user(self, email, password, **extra_fields):
        if not email or not password:
            raise ValueError
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""

    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    surname = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'


class Ticket(models.Model):
    """Single ticket in system."""

    PRIORITY_CHOICES = [
        ('LOW', 'Low'),
        ('MODERATE', 'Moderate'),
        ('URGENT', 'Urgent')
    ]

    STATUS_CHOICES = [
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('CLOSED', 'Closed'),
    ]

    created_by = models.ForeignKey('User', on_delete=models.PROTECT)
    assigned_to = models.ForeignKey(
        'User', on_delete=models.PROTECT, related_name='tickets')
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='OPEN')
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    priority = models.CharField(
        max_length=255, choices=PRIORITY_CHOICES, default='LOW')

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    author = models.ForeignKey('User', on_delete=models.SET_NULL, null=True)
    ticket = models.ForeignKey('Ticket', on_delete=models.CASCADE)
    created_date = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField(auto_now=True)
    text = models.TextField()

    def __str__(self) -> str:
        return f'{self.ticket.id}_{self.text[:20]}'
