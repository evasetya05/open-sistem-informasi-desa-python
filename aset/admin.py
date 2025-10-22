from django.contrib import admin
from .models import Aset

@admin.register(Aset)
class AsetAdmin(admin.ModelAdmin):
    list_display = ("nama", "jenis", "sub_kategori", "penduduk", "pemilik_luar", "tahun_data")
    list_filter = ("jenis", "pemilik_luar", "tahun_data")
    search_fields = ("nama", "no_sppt", "no_ktp", "desa")
