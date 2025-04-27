"""
Possibly Deprecated Model, this appears to be superseded by Capture
"""
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Plant(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # User who captured the plant
    name = models.CharField(max_length=100)  # Plant name
    scientific_name = models.CharField(max_length=150, blank=True, null=True)  # Optional scientific name
    description = models.TextField(blank=True)  # Short description of the plant
    location = models.CharField(max_length=255, blank=True, null=True)  # Locations plant is found
    date_added = models.DateTimeField(auto_now_add=True)  # Timestamp when the plant was added

    def __str__(self):
        return self.name
