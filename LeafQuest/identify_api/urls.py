from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.make_request),
    path('return/', views.return_ident),
]