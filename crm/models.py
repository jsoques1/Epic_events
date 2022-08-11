from django.conf import settings
from django.db import models

from users.models import SalesUser, SupportUser


class Customer(models.Model):
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    email = models.EmailField(max_length=100)

    company_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    sales_contact = models.ForeignKey(
        SalesUser,
        on_delete=models.CASCADE
    )
    is_client = models.BooleanField(default=False)

    def __str__(self):
        return f"Customer {self.last_name} {self.first_name} is client ? {self.is_client}"


class Contract(models.Model):
    sales_contact = models.ForeignKey(
        SalesUser,
        on_delete=models.CASCADE,
    )
    client = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    amount = models.FloatField()
    payment_due = models.DateField()
    is_signed = models.BooleanField(default=False)

    def __str__(self):

        return f"Contract {self.date_updated} {self.client.last_name}, " \
               f"{self.client.first_name} is signed ? {self.is_signed}"


class Event(models.Model):
    contract = models.OneToOneField(
        Contract,
        on_delete=models.CASCADE
    )
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)

    support = models.ForeignKey(
        SupportUser,
        on_delete=models.CASCADE,
    )
    event_status = models.BooleanField(default=False, verbose_name="Completed")
    attendees = models.PositiveIntegerField()
    event_date = models.DateTimeField()
    notes = models.CharField(max_length=100)

    def __str__(self):
        return f"Event {self.event_date} {self.contract.client.last_name} {self.contract.client.first_name}"
