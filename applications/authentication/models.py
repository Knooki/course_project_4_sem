from django.db import models
from django.contrib.auth.models import AbstractUser



class CustomUser(AbstractUser):
    is_customer = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    country = models.TextField(default='Беларусь')