"""
URLs for identify_api
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.make_request),
    path('return/', views.return_ident),
]
