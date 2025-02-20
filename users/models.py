from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import timedelta, datetime

MEMBERSHIP_TYPES = {
    'Silver': 30,  # 30 days validity
    'Gold': 90,    # 90 days validity
    'Diamond': 180 # 180 days validity
}

class User(AbstractUser):
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    phone_number = models.CharField(max_length=15, unique=True)
    membership_type = models.CharField(max_length=10, choices=[(k, k) for k in MEMBERSHIP_TYPES.keys()], null=True, blank=True)
    membership_start_date = models.DateTimeField(null=True, blank=True)
    membership_expiry_date = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def activate_membership(self, membership_type):
        """Activate membership and set start and expiry dates"""
        self.membership_type = membership_type
        self.membership_start_date = datetime.now()
        self.membership_expiry_date = self.membership_start_date + timedelta(days=MEMBERSHIP_TYPES[membership_type])
        self.save()

    def __str__(self):
        return self.phone_number
