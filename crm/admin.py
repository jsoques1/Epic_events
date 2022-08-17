from django.contrib import admin
from .models import Customer, Contract, Event

import logging
logger = logging.getLogger(__name__)


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity',
         {'fields': ('company_name', 'first_name', 'last_name', 'email', 'phone_number', 'mobile_number')}),
        ('Dates', {'fields': ('date_created', 'date_updated')}),
        ('Client', {'fields': ('is_client', 'salesman')}),
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('company_name', 'first_name', 'last_name', 'email', 'phone_number',
                    'mobile_number', 'is_client', 'salesman')
    list_filter = ['is_client', 'salesman']
    search_fields = ('company_name', 'first_name', 'last_name', 'email')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ('customer', 'amount', 'payment_due')}),
        ('Sales', {'fields': ('is_signed', 'salesman')}),
        ('Info', {'fields': ('date_created', 'date_updated')})
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('id', 'customer', 'amount', 'payment_due', 'is_signed', 'salesman')
    list_filter = ['is_signed', 'salesman']
    search_fields = ('id', 'customer')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details',
         {'fields': ('name', 'location', 'contract', 'attendees', 'event_date', 'event_status')}),
        ('Support', {'fields': ('support', 'notes')}),
        ('Info', {'fields': ('date_created', 'date_updated')})
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('name', 'contract', 'location', 'support', 'attendees', 'event_date', 'event_status')
    list_filter = ('event_status', 'support')
    search_fields = ('name', 'client', 'location')
