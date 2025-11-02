from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from .models import Penduduk, KartuKeluarga


# --- Inline untuk menampilkan anggota keluarga di admin KartuKeluarga ---
class AnggotaInline(admin.TabularInline):
    model = Penduduk
    extra = 0
    fields = ('nik', 'nama_lgkp', 'stat_hbkel_1', 'jenis_klmin', 'tgl_lhr')
    readonly_fields = ('nik', 'nama_lgkp', 'jenis_klmin', 'tgl_lhr')
    can_delete = False
    show_change_link = True


# --- Admin Kartu Keluarga ---
@admin.register(KartuKeluarga)
class KartuKeluargaAdmin(admin.ModelAdmin):
    list_display = ('no_kk', 'kepala_keluarga_nama', 'alamat', 'no_rt', 'no_rw')
    inlines = [AnggotaInline]

    def kepala_keluarga_nama(self, obj):
        if obj.kepala_keluarga:
            return obj.kepala_keluarga.nama_lgkp
        return "-"
    kepala_keluarga_nama.short_description = "Kepala Keluarga"


# --- Resource untuk Import/Export Penduduk ---
class PendudukResource(resources.ModelResource):
    no_kk = fields.Field(attribute='no_kk', column_name='NO_KK')
    nik = fields.Field(attribute='nik', column_name='NIK')
    nama_lgkp = fields.Field(attribute='nama_lgkp', column_name='NAMA_LGKP')
    jenis_klmin = fields.Field(attribute='jenis_klmin', column_name='JENIS_KLMIN')
    jenis_klmin_ket = fields.Field(attribute='jenis_klmin_ket', column_name='JENIS_KLMIN_KET')
    tmpt_lhr = fields.Field(attribute='tmpt_lhr', column_name='TMPT_LHR')
    tgl_lhr = fields.Field(attribute='tgl_lhr', column_name='TGL_LHR')
    agama = fields.Field(attribute='agama', column_name='AGAMA')
    agama_ket = fields.Field(attribute='agama_ket', column_name='AGAMA_KET')
    pddk_akh = fields.Field(attribute='pddk_akh', column_name='PDDK_AKH')
    pendidikan_akh_ket = fields.Field(attribute='pendidikan_akh_ket', column_name='PENDIDIKAN_AKH_KET')
    jenis_pkrjn = fields.Field(attribute='jenis_pkrjn', column_name='JENIS_PKRJN')
    jenis_pkrjn_ket = fields.Field(attribute='jenis_pkrjn_ket', column_name='JENIS_PKRJN_KET')
    gol_drh = fields.Field(attribute='gol_drh', column_name='GOL_DRH')
    stat_kwn_ket = fields.Field(attribute='stat_kwn_ket', column_name='STAT_KWN_KET')
    tgl_kwn = fields.Field(attribute='tgl_kwn', column_name='TGL_KWN')
    stat_hbkel = fields.Field(attribute='stat_hbkel', column_name='STAT_HBKEL')
    stat_hbkel_1 = fields.Field(attribute='stat_hbkel_1', column_name='STAT_HBKEL_1')
    alamat = fields.Field(attribute='alamat', column_name='ALAMAT')
    no_rt = fields.Field(attribute='no_rt', column_name='NO_RT')
    no_rw = fields.Field(attribute='no_rw', column_name='NO_RW')
    dusun = fields.Field(attribute='dusun', column_name='DUSUN')
    kode_pos = fields.Field(attribute='kode_pos', column_name='KODE_POS')
    telp = fields.Field(attribute='telp', column_name='TELP')
    no_prop = fields.Field(attribute='no_prop', column_name='NO_PROP')
    nama_prop = fields.Field(attribute='nama_prop', column_name='NAMA_PROP')
    no_kab = fields.Field(attribute='no_kab', column_name='NO_KAB')
    nama_kab = fields.Field(attribute='nama_kab', column_name='NAMA_KAB')
    no_kec = fields.Field(attribute='no_kec', column_name='NO_KEC')
    nama_kec = fields.Field(attribute='nama_kec', column_name='NAMA_KEC')
    no_kel = fields.Field(attribute='no_kel', column_name='NO_KEL')
    nama_kel = fields.Field(attribute='nama_kel', column_name='NAMA_KEL')

    class Meta:
        model = Penduduk
        import_id_fields = ['nik']
        skip_unchanged = True
        report_skipped = True


# --- Admin Penduduk utama ---
@admin.register(Penduduk)
class PendudukAdmin(ImportExportModelAdmin):
    resource_class = PendudukResource

    # ✅ tampilkan semua kolom otomatis di admin list
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]

    search_fields = ('nik', 'nama_lgkp', 'nama_kab', 'nama_kec', 'nama_kel')
    list_filter = ('jenis_klmin_ket', 'nama_kab', 'nama_kec', 'nama_kel')
    list_per_page = 100
