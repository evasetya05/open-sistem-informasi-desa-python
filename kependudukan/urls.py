from django.urls import path
from . import views

urlpatterns = [
    # Kartu Keluarga
    path('kk/', views.kk_list, name='kk_list'),
    path('kk/add/', views.kk_add, name='kk_add'),
    path('kk/<int:pk>/', views.kk_detail, name='kk_detail'),

    # Penduduk
    path('penduduk/', views.penduduk_list, name='penduduk_list'),
    path('penduduk/add/', views.penduduk_add, name='penduduk_add'),
    path('penduduk/<int:pk>/', views.penduduk_detail, name='penduduk_detail'),
]
