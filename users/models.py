from django.db import models
from django.contrib.auth import get_user_model

IT = 'IT'
SALES = 'SALES'
SUPPORT = 'SUPPORT'

User = get_user_model()


class CrmUser(User):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    phone_number = models.CharField(max_length=20)
    mobile_number = models.CharField(max_length=20)
    role = models.CharField(
        [
            (IT, IT),
            (SALES, SALES),
            (SUPPORT, SUPPORT),
        ],
        max_length=7,
        default=IT
    )

    def __str__(self):
        print(f'username={self.username}, role={self.role}')


class ItUser(CrmUser):
    role = IT


class SalesUser(CrmUser):
    role = SALES


class SupportUser(CrmUser):
    role = SUPPORT
