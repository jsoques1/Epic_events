from django.conf import settings
from django.db import models
from users.models import SALES, SUPPORT, MGMT

import logging
logger = logging.getLogger(__name__)


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)

    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    salesman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': MGMT},
        null=True,
    )
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.company_name}"


class Contract(models.Model):
    salesman = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': SALES},
        null=True,
    )
    client = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        null=True,
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_due = models.DateField()
    is_signed = models.BooleanField(default=False)

    def __str__(self):
        return f"Contract #{self.id} - {self.client.first_name}" \
               f"{self.client.last_name} - {self.client.company_name}"


class Event(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE,
        null=True,
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100, null=False)
    location = models.CharField(max_length=100)

    support = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': SUPPORT},
        null=True,
    )
    event_status = models.BooleanField(default=False, verbose_name="Completed")
    attendees = models.PositiveIntegerField()
    event_date = models.DateTimeField()
    notes = models.TextField(max_length=800, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"
