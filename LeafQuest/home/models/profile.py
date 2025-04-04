from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


# user profile/account
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default=' ')
    aboutMe = models.TextField(max_length=250, blank=True)
    pfp = models.ImageField(upload_to='profile/', blank=True, default='profile/defaultprofile.png')
    private = models.BooleanField(default=False)

    # more readable name for model
    def __str__(self):
        return self.user.username + ' (' + self.name + ')'
