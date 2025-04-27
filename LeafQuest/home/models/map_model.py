"""
Models for google maps integration
"""
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class MapPin(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    lat = models.FloatField()
    lng = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.lat}, {self.lng})"
