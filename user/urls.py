from django.urls import path
from . import views

urlpatterns = [
    path('manage/', views.manage_users, name='manage_users'),
]
