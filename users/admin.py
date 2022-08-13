from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import Group
from django.contrib.admin.models import LogEntry

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


# @admin.register(LogEntry)
# class LogEntryAdmin(admin.ModelAdmin):
#     date_hierarchy = "action_time"
#     # to filter the results
#     list_filter = ["user", "content_type", "action_flag"]
#     # when searching the user will be able to search in both object_repr and change_message
#     search_fields = ["object_repr", "change_message"]
#
#     list_display = [
#         "action_time",
#         "user",
#         "content_type",
#         "action_flag",
#     ]
#
#     def has_add_permission(self, request):
#         # only superuser can read the history
#         return request.user.is_superuser
#
#     def has_change_permission(self, request, obj=None):
#         return request.user.is_superuser
#
#     def has_delete_permission(self, request, obj=None):
#         return request.user.is_superuser
#
#     def has_view_permission(self, request, obj=None):
#         return request.user.is_superuser
