from django.urls import path
from .views import home_view, profile_view

urlpatterns = [
    path('', home_view, name="home"),
    path('profile', profile_view, name="profile"),
    path('capture', capture_view, name="capture"),
    path('plantdex', plantdex_view, name="plantdex"),
    path('badges', badges_view, name="badges"),
    path('map', map_view, name="map"),
    path('social', social_view, name="social"),
    path('settings', settings_view, name="settings"),
    path('logout', logout_view, name="logout"),
    path('about', about_view, name="about")
]