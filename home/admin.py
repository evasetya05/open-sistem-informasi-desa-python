from django.contrib import admin
from .models import PostingInvestasi

@admin.register(PostingInvestasi)
class PostingInvestasiAdmin(admin.ModelAdmin):
    list_display = ("judul", "slug", "tanggal_terbit")  # kolom yang tampil di admin
    search_fields = ("judul",)  # pencarian berdasarkan judul
    prepopulated_fields = {"slug": ("judul",)}  # slug otomatis dari judul
