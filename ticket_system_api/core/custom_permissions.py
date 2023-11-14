"""
Custom permisions for views and objects.
"""

from rest_framework import permissions


class IsOwnerOrAdminOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return (getattr(obj, 'author', None) == request.user or getattr(obj, 'created_by', None) == request.user) or request.user.is_superuser
