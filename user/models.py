from django.contrib.auth.models import AbstractUser
from django.db import models

User_type_choice = (
    ('Admin', 'Admin'),
    ('Operator', 'Operator'),
    ('Customer', 'Customer'),
)


class User(AbstractUser):
    user_type = models.CharField(choices=User_type_choice, max_length=25, default='Customer')
    phone_number = models.CharField(max_length=13, unique=True, null=True, blank=True)

    def __str__(self):
        return self.username
