from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    aboutMe = models.TextField(blank=True)

    def __str__(self):
        return self.name + '(' + self.user.username + ')'


