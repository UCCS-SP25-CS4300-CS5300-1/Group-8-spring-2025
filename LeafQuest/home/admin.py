from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(Profile)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Badge)
admin.site.register(CapturedImage)