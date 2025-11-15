from django.db import models


from django.db import models

class KartuKeluarga(models.Model):
    no_kk = models.CharField("Nomor KK", max_length=20, unique=True)
    alamat = models.TextField(blank=True, null=True)
    no_rt = models.CharField("RT", max_length=5, blank=True, null=True)
    no_rw = models.CharField("RW", max_length=5, blank=True, null=True)
    kode_pos = models.CharField("Kode Pos", max_length=10, blank=True, null=True)

    # KK asal = hubungan parent ke KK lain
    parent = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='children',
        verbose_name="KK Induk / Asal"
    )

    def __str__(self):
        return self.no_kk

    @property
    def kepala_keluarga(self):
        # Mengambil Penduduk yang statusnya kepala keluarga
        return self.penduduk_set.filter(stat_hbkel_1__icontains="Kepala Keluarga").first()

    @property
    def kepala_stat_hbkel(self):
        # Mengambil stat_hbkel_1 dari kepala keluarga
        kepala = self.kepala_keluarga
        return kepala.stat_hbkel_1 if kepala else None

    @property
    def kepala_alamat(self):
        # Mengambil alamat dari kepala keluarga
        kepala = self.kepala_keluarga
        return kepala.alamat if kepala else None
    
    @property
    def kepala_no_rt(self):
        kepala = self.kepala_keluarga
        return kepala.no_rt if kepala else None

    @property
    def kepala_no_rw(self):
        kepala = self.kepala_keluarga
        return kepala.no_rw if kepala else None




class Penduduk(models.Model):
    

    no_kk = models.ForeignKey(KartuKeluarga, on_delete=models.SET_NULL, null=True, blank=True, related_name='penduduk_set')

    nik = models.CharField("NIK", max_length=20, unique=True)
    nama_lgkp = models.CharField("Nama Lengkap", max_length=100)
    jenis_klmin = models.CharField("Jenis Kelamin", max_length=1, choices=[('L', 'Laki-Laki'), ('P', 'Perempuan')])
    jenis_klmin_ket = models.CharField("Keterangan Jenis Kelamin", max_length=20, blank=True, null=True)
    tmpt_lhr = models.CharField("Tempat Lahir", max_length=50)
    tgl_lhr = models.DateField("Tanggal Lahir")
    agama = models.CharField("Agama (kode)", max_length=10, blank=True, null=True)
    agama_ket = models.CharField("Agama", max_length=50)
    pddk_akh = models.CharField("Kode Pendidikan", max_length=10, blank=True, null=True)
    pendidikan_akh_ket = models.CharField("Pendidikan Terakhir", max_length=50)
    jenis_pkrjn = models.CharField("Kode Pekerjaan", max_length=10, blank=True, null=True)
    jenis_pkrjn_ket = models.CharField("Pekerjaan", max_length=50)
    gol_drh = models.CharField("Golongan Darah", max_length=5, blank=True, null=True)
    stat_kwn_ket = models.CharField("Status Kawin", max_length=30)
    tgl_kwn = models.DateField("Tanggal Kawin", blank=True, null=True)
    stat_hbkel = models.CharField("Status Hubungan Keluarga (kode)", max_length=10, blank=True, null=True)
    stat_hbkel_1 = models.CharField("Hubungan Keluarga", max_length=30)
    alamat = models.TextField()
    no_rt = models.CharField("RT", max_length=5)
    no_rw = models.CharField("RW", max_length=5)
    dusun = models.CharField("Dusun", max_length=50, blank=True, null=True)
    kode_pos = models.CharField("Kode Pos", max_length=10, blank=True, null=True)
    telp = models.CharField("No Telepon", max_length=20, blank=True, null=True)
    no_prop = models.CharField("Kode Provinsi", max_length=5)
    nama_prop = models.CharField("Nama Provinsi", max_length=50)
    no_kab = models.CharField("Kode Kabupaten", max_length=5)
    nama_kab = models.CharField("Nama Kabupaten", max_length=50)
    no_kec = models.CharField("Kode Kecamatan", max_length=5)
    nama_kec = models.CharField("Nama Kecamatan", max_length=50)
    no_kel = models.CharField("Kode Kelurahan", max_length=5)
    nama_kel = models.CharField("Nama Kelurahan", max_length=50)
    status_hidup = models.BooleanField("Hidup", default=True)
    tgl_meninggal = models.DateField("Tanggal Meninggal", blank=True, null=True)

    def __str__(self):
        return f"{self.nama_lgkp} ({self.nik})"

