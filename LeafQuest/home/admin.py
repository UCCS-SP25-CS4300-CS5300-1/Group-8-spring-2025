"""
Register Models for Admin Interface
"""
from django.contrib import admin
from .models import Profile, FriendList, FriendRequest, Badge, CapturedImage, Leaderboard

# Register your models here.

admin.site.register(Profile)
admin.site.register(FriendList)
admin.site.register(FriendRequest)
admin.site.register(Badge)
admin.site.register(CapturedImage)
admin.site.register(Leaderboard)
