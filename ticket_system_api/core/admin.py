"""
Customization of admin page.
"""

from django.contrib import admin
from core import models
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _
# Register your models here.


class UserAdmin(BaseUserAdmin):
    """Defines admin page for users."""
    ordering = ['id']
    list_display = ['email', 'name', 'surname']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        (
            _('Permissions'),
            {
                'fields': (
                    'is_active',
                    'is_staff',
                    'is_superuser',
                )
            }
        )
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'name',
                'surname',
                'is_active',
                'is_staff',
                'is_superuser'
            )
        }),
    )
    list_filter = ['is_active', 'is_staff', 'is_superuser']


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Ticket)
admin.site.register(models.Comment)
