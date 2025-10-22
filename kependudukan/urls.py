from django.urls import path
from . import views

urlpatterns = [
    # Kartu Keluarga
    path('kk/', views.kk_list, name='kk_list'),
    path('kk/add/', views.kk_add, name='kk_add'),
    path('kk/<int:pk>/', views.kk_detail, name='kk_detail'),
    path('kk/export/', views.kk_export_xlsx, name='kk_export_xlsx'),

    # Penduduk
    path('penduduk/', views.penduduk_list, name='penduduk_list'),
    path('penduduk/add/', views.penduduk_add, name='penduduk_add'),
    path('penduduk/<int:pk>/edit/', views.penduduk_edit, name='penduduk_edit'),
    path('penduduk/<int:pk>/', views.penduduk_detail, name='penduduk_detail'),
    path('penduduk/export/', views.penduduk_export_xlsx, name='penduduk_export_xlsx'),
]
