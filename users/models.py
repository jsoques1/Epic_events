from django.db import models
from django.contrib.auth.models import AbstractUser
import logging
logger = logging.getLogger(__name__)

MGMT = 'MGMT'
SALES = 'SALES'
SUPPORT = 'SUPPORT'


class User(AbstractUser):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20)
    role = models.CharField(choices=
        [
            (MGMT, MGMT),
            (SALES, SALES),
            (SUPPORT, SUPPORT),
        ],
        max_length=7,
        default=MGMT
    )

    def __str__(self):
        return f'{self.username} - {self.role}'
