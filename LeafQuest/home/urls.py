from django.urls import include, path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

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
    path('about', about_view, name="about"),

    # account management
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', registerPage, name='register_page'),
    path('accounts/profile/', userPage, name='user-page'),

    path('users/<int:pk>', ProfileDetailView.as_view(), name= 'profile_detail'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this allows uploaded images to load correctly
