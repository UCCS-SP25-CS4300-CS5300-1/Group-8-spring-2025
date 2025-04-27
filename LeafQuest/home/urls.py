"""
URLs for home
"""
from django.views.static import serve
from django.urls import path, re_path
from django.conf.urls.static import static
from django.conf import settings

from .views import home_view, capture_view, badges_view, map_view, social_view, profile_search_view, profile_search, \
    leaderboard_view, friend_list, profile_redir, profile_view, add_friend, edit_profile, cancel_friend, \
    remove_friend, accept_req, decline_req, settings_view, logout_view, about_view, register_view, login_view, map_views

from .views.plantdex import plantdex_detail_view, plantdex_view


urlpatterns = [

    re_path(r'^media/(?P<path>.*)$', serve, {
        'document_root': settings.MEDIA_ROOT,  # Evil ugly garbage, thanks lazy Django devs
    }),

    path('api/', home_view, name="api"),
    path('', home_view, name="home"),
    path('capture/', capture_view, name="capture"),
    path('badges/', badges_view, name="badges"),
    path('map/', map_view, name="map"),

    path('plantdex/', plantdex_view, name="plantdex"),
    path('plantdex/<pk>/', plantdex_detail_view, name="plantdex_detail"),

    # social features
    path('social/', social_view, name="social"),
    path('social/search/', profile_search_view, name="search"),
    path('social/search/results/', profile_search, name="search_results"),
    path('social/leaderboard/', leaderboard_view, name="leaderboard_view"),
    path('social/friends', friend_list, name='friend_list'),

    # profile viewing/editing
    path('profile/', profile_redir, name="profile"),
    path('profile/<int:profile_id>', profile_view, name='profile_view'),
    path('profile/edit', edit_profile, name='edit_profile'),

    # friend request views - no templates, just code to handle friend management
    path('profile/<int:profile_id>/add', add_friend, name='add_friend'),
    path('profile/<int:profile_id>/cancel', cancel_friend, name='cancel_friend'),
    path('profile/<int:profile_id>/remove', remove_friend, name='remove_friend'),
    path('profile/friends/accept/<int:request_id>', accept_req, name='accept_req'),
    path('profile/friends/decline/<int:request_id>', decline_req, name='decline_req'),

    path('settings/', settings_view, name="settings"),
    path('logout/', logout_view, name="logout"),
    path('about/', about_view, name="about"),

    # account management
    path('accounts/register/', register_view, name='register'),
    path('accounts/login/', login_view, name='login'),
    path('accounts/logout/', logout_view, name='logout'),

    # map pins
    path('api/pins/', map_views.get_user_pins, name='get_pins'),
    path('api/pins/save/', map_views.save_pin, name='save_pin'),
    path('api/pins/<int:pin_id>/edit/', map_views.update_pin, name='edit_pin'),
    path('api/pins/<int:pin_id>/delete/', map_views.delete_pin, name='delete_pin')

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # this allows uploaded images to load correctly
