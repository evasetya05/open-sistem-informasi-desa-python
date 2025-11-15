from django.db import models
from django.utils import timezone
from django.urls import reverse

# Pilihan angka 1–15 sebagai string (untuk CharField)
RT_RW_CHOICES = [(str(i), f"{i:02}") for i in range(1, 51)]

class AntrianSession(models.Model):
    tanggal = models.DateField(default=timezone.now)
    aktif = models.BooleanField(default=True)
    kegiatan = models.CharField(max_length=255)  # Tambahan kegiatan

    def __str__(self):
        return f"Antrian {self.tanggal} - {'Aktif' if self.aktif else 'Tidak Aktif'}"

class Antrian(models.Model):
    session = models.ForeignKey(AntrianSession, on_delete=models.CASCADE)
    nomor = models.PositiveIntegerField()
    nama = models.CharField(max_length=100)
    nik = models.CharField(max_length=16, blank=True, null=True)
    rt = models.CharField(max_length=2, choices=RT_RW_CHOICES, blank=True, null=True)
    rw = models.CharField(max_length=2, choices=RT_RW_CHOICES, blank=True, null=True)
    waktu_daftar = models.DateTimeField(auto_now_add=True)
    Keterangan = models.CharField(max_length=100, blank=True, null=True)
    sudah_dipanggil = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nomor} - {self.nama}"

    def get_absolute_url(self):
        return reverse('detail_antrian', kwargs={'pk': self.pk})
