from django.db import models
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField  # Import CKEditor

class PostingInvestasi(models.Model):
    judul = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    isi = RichTextUploadingField(blank=True, null=True)  # Ganti TextField → CKEditor
    gambar = models.ImageField(upload_to='berita_gambar/', blank=True, null=True)
    tanggal_terbit = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.judul

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.judul)
        super().save(*args, **kwargs)
