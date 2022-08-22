from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group

import logging
logger = logging.getLogger(__name__)

admin.site.unregister(Group)


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        ('Identity',
         {'fields': ('username', 'first_name', 'last_name', 'email', 'phone_number',
                     'mobile_number')}),
        ('Role', {'fields': ('role',)}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number',
                    'mobile_number', 'role',)
