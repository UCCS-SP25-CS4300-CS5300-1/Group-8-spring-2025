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

    path('profile/', userPage, name='user_page'),
    path('profile/friends', friend_list, name='friend_list'),
    path('profile/friends/accept/<int:request_id>', accept_req, name='accept_req'),
    path('profile/friends/decline/<int:request_id>', decline_req, name='decline_req'),

    path('users/<int:profile_id>', profile_detail, name= 'profile_detail'),
    path('users/<int:profile_id>/add', add_friend, name='add_friend'),
    path('users/<int:profile_id>/cancel', cancel_friend, name='cancel_friend'),
    #path('users/<int:profile_id>/remove', remove_friend, name='remove_friend'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this allows uploaded images to load correctly
