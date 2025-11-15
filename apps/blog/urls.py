from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('create/', views.create_blog, name='create_blog'),  # Blog create URL
    path('', views.blog_list, name='blog_list'),    # Blog list URL
]
