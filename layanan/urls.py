from django.urls import path
from . import views
from layanan.views.antrian import AntrianDetailView, buat_kegiatan_antrian, lihat_nomor



urlpatterns = [
    path('daftar/', views.daftar_antrian, name='daftar_antrian'),
    path('antrian/<int:pk>/', AntrianDetailView.as_view(), name='detail_antrian'),
    path('panggil/', views.panggil_antrian, name='panggil_antrian'),
    path('lihat_nomor/<int:pk>/', views.lihat_nomor, name='lihat_nomor'),
    path('antrian/buat/', buat_kegiatan_antrian, name='buat_kegiatan_antrian'),
    path('antrian/session/<int:session_id>/', views.daftar_antrian, name='daftar_antrian_dengan_session'),
    path('antrian/riwayat/', views.riwayat_antrian, name='riwayat_antrian'),

]
