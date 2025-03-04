from django.urls import path
from .views import home_view, profile_view

urlpatterns = [
    path('', home_view, name="home"),
    path('profile', profile_view, name="profile")
]
