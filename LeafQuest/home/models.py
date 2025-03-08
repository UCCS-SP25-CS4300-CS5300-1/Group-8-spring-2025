from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    aboutMe = models.TextField(max_length=250, blank=True)
    pfp = models.ImageField(upload_to='profile/', blank=True)
    # to be added - friends

    def __str__(self):
        return self.name + '(' + self.user.username + ')'


