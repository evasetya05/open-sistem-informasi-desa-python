# forms.py
from django import forms
from .models import PostingInvestasi

class PostingInvestasiForm(forms.ModelForm):
    class Meta:
        model = PostingInvestasi
        fields = ['judul', 'isi', 'gambar']  # pastikan 'gambar' masuk di sini
