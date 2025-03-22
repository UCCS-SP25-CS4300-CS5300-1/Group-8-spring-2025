from django.db import models
from django.contrib.auth.models import User

class Badge(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100) 
    description = models.TextField(blank=True) 
    #image = models.ImageField(upload_to='badge_images/')  

    def __str__(self):
        return self.name
