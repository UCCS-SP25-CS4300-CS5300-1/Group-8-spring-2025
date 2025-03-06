from django.urls import include, path
from .views import *

urlpatterns = [
    path('', home_view, name="home"),
    path('profile', profile_view, name="profile"),

    # account management
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', registerPage, name='register_page')
]
