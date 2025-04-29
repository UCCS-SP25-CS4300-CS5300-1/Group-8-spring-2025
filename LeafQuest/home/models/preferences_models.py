"""
Models for storing user preferences.
"""

from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class ClientPreferences(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    use_dark_mode = models.BooleanField(default=False)
