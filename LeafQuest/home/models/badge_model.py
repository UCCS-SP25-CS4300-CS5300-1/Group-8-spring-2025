"""
Models for unlockable Badges
"""
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class Badge(models.Model):
    users = models.ManyToManyField(User, blank=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='badges/', default='badges/default_image.png')

    def __str__(self):
        return self.name
