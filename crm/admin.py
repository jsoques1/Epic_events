from django.contrib import admin
from .models import Customer, Contract, Event


@admin.register(Customer)
class ClientAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Identity',
         {'fields': ('first_name', 'last_name', 'company_name', 'email', 'phone', 'mobile')}),
        ('Dates', {'fields': ('date_created', 'date_updated')}),
        ('Client', {'fields': ['is_client']}),
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('first_name', 'last_name', 'company_name', 'email', 'phone_number',
                    'mobile_number', 'is_client')
    list_filter = ['is_client']
    search_fields = ('first_name', 'last_name', 'company_name')


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    fieldsets = (
        ('', {'fields': ('client', 'amount', 'payment_due')}),
        ('Sales', {'fields': ['is_signed']}),
        ('Info', {'fields': ('date_created', 'date_updated')})
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('id', 'client', 'amount', 'payment_due', 'is_signed')
    list_filter = ['is_signed']
    search_fields = ('id', 'client__last_name')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fieldsets = (
        ('Details',
         {'fields': ('name', 'location', 'contract', 'attendees', 'event_date', 'event_status')}),
        ('Support', {'fields': ('support_contact', 'notes')}),
        ('Info', {'fields': ('date_created', 'date_updated')})
    )
    readonly_fields = ('date_created', 'date_updated')
    list_display = ('name', 'location', 'contract', 'support', 'attendees', 'event_date', 'event_status')
    list_filter = ('event_status', 'support')
    search_fields = ('name', 'location', 'client__last_name')
