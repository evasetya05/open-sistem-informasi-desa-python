from django.contrib import admin
from .models import PostingInvestasi


@admin.register(PostingInvestasi)
class BeritaAdmin(admin.ModelAdmin):
    list_display = ['judul', 'isi', 'tanggal_terbit']