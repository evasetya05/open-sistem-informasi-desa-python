from django.db import models
from kependudukan.models import Penduduk

class Aset(models.Model):
    JENIS_CHOICES = [
        ('tanah', 'Tanah'),
        ('bangunan', 'Bangunan'),
        ('kendaraan', 'Kendaraan'),
        ('ternak', 'Ternak'),
        ('pertanian', 'Pertanian'),
        ('usaha', 'Usaha'),
        ('lainnya', 'Lainnya'),
    ]

    jenis = models.CharField(max_length=20, choices=JENIS_CHOICES)
    sub_kategori = models.CharField(max_length=100, blank=True, null=True)
    nama = models.CharField(max_length=255)

    no_ktp = models.CharField(max_length=50, blank=True, null=True)
    alamat = models.CharField(max_length=255, blank=True, null=True)
    rt_rw = models.CharField(max_length=20, blank=True, null=True)
    desa = models.CharField(max_length=100, blank=True, null=True)
    kecamatan = models.CharField(max_length=100, blank=True, null=True)
    pekerjaan = models.CharField(max_length=100, blank=True, null=True)

    lokasi_lahan = models.CharField(max_length=255, blank=True, null=True)

    # bidang tanah
    no_sppt = models.CharField(max_length=100, blank=True, null=True)
    no_c_petok = models.CharField(max_length=100, blank=True, null=True)
    persil = models.CharField(max_length=100, blank=True, null=True)
    kelas = models.CharField(max_length=50, blank=True, null=True)
    nama_c = models.CharField(max_length=100, blank=True, null=True)
    luasc = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    luas_mohon = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    luas_sppt = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    nib = models.CharField(max_length=50, blank=True, null=True)
    utara = models.CharField(max_length=255, blank=True, null=True)
    timur = models.CharField(max_length=255, blank=True, null=True)
    selatan = models.CharField(max_length=255, blank=True, null=True)
    barat = models.CharField(max_length=255, blank=True, null=True)

    # umum
    jumlah = models.PositiveIntegerField(blank=True, null=True)
    nilai_taksiran = models.DecimalField(max_digits=15, decimal_places=2, blank=True, null=True)
    keterangan = models.TextField(blank=True, null=True)

    penduduk = models.ForeignKey(Penduduk, on_delete=models.SET_NULL, blank=True, null=True)
    pemilik_luar = models.BooleanField(default=False)
    tahun_data = models.PositiveIntegerField(default=2025)

    class Meta:
        verbose_name = "Aset"
        verbose_name_plural = "Daftar Aset"
        ordering = ["-tahun_data", "nama"]

    def __str__(self):
        return f"{self.nama} ({self.get_jenis_display()})"
