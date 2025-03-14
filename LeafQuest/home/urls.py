from django.urls import include, path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home_view, name="home"),

    # profile viewing/editing and friends list
    path('profile/<int:profile_id>', profile_view, name="profile"),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/friends', friend_list, name='friend_list'),

    # friend request views - no templates, just code to handle friend management
    path('profile/<int:profile_id>/add', add_friend, name='add_friend'),
    path('profile/<int:profile_id>/cancel', cancel_friend, name='cancel_friend'),
    #path('users/<int:profile_id>/remove', remove_friend, name='remove_friend'),
    path('profile/friends/accept/<int:request_id>', accept_req, name='accept_req'),
    path('profile/friends/decline/<int:request_id>', decline_req, name='decline_req'),

    path('capture', capture_view, name="capture"),
    path('plantdex', plantdex_view, name="plantdex"),
    path('badges', badges_view, name="badges"),
    path('map', map_view, name="map"),
    path('social', social_view, name="social"),
    path('settings', settings_view, name="settings"),
    path('logout', logout_view, name="logout"),
    path('about', about_view, name="about")
]