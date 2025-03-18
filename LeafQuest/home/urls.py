from django.urls import include, path
from .views import *
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    # API routes
    path('api/', home_view, name="api_home"),
    path('api/profile', profile_view, name="api_profile"),

    path('', home_view, name="home"),
    path('capture', capture_view, name="capture"),
    path('plantdex', plantdex_view, name="plantdex"),
    path('badges', badges_view, name="badges"),
    path('map', map_view, name="map"),
    path('social', social_view, name="social"),

    # profile viewing/editing and friends list
    path('profile', profile_redir, name="profile"),
    path('profile/<int:profile_id>', profile_view, name='profile_view'),
    path('profile/edit', edit_profile, name='edit_profile'),
    path('profile/friends', friend_list, name='friend_list'),

    # friend request views - no templates, just code to handle friend management
    path('profile/<int:profile_id>/add', add_friend, name='add_friend'),
    path('profile/<int:profile_id>/cancel', cancel_friend, name='cancel_friend'),
    path('profile/<int:profile_id>/remove', remove_friend, name='remove_friend'),
    path('profile/friends/accept/<int:request_id>', accept_req, name='accept_req'),
    path('profile/friends/decline/<int:request_id>', decline_req, name='decline_req'),

    path('settings', settings_view, name="settings"),
    path('logout', logout_view, name="logout"),
    path('about', about_view, name="about"),

    # account management
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) # this allows uploaded images to load correctly
