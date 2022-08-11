from django.contrib import admin
from .models import ItUser, SalesUser, SupportUser


@admin.register(ItUser)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity',
         {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')


@admin.register(SalesUser)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity',
         {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')


@admin.register(SupportUser)
class CustomUserAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity',
         {'fields': ('username', 'password', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')