from django import forms
from .models import Penduduk, KartuKeluarga

from django import forms
from .models import KartuKeluarga, Penduduk

class KartuKeluargaForm(forms.ModelForm):
    class Meta:
        model = KartuKeluarga
        fields = ['no_kk', 'alamat', 'no_rt', 'no_rw', 'kode_pos', 'parent']
        labels = {
            'no_kk': 'Nomor KK',
            'alamat': 'Alamat',
            'no_rt': 'RT',
            'no_rw': 'RW',
            'kode_pos': 'Kode Pos',
            'parent': 'KK Induk (Asal)',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dropdown parent menampilkan no_kk + kepala keluarga
        self.fields['parent'].queryset = KartuKeluarga.objects.all().order_by('no_kk')
        self.fields['parent'].required = False
        self.fields['parent'].empty_label = "— Tidak ada (KK utama) —"
        self.fields['parent'].label_from_instance = lambda obj: f"{obj.no_kk} - {obj.kepala_keluarga or 'Tanpa Kepala'}"



class PendudukForm(forms.ModelForm):
    class Meta:
        model = Penduduk
        fields = [
            'nik', 'nama_lgkp', 'jenis_klmin', 'jenis_klmin_ket', 'tmpt_lhr', 'tgl_lhr',
            'agama', 'agama_ket', 'pddk_akh', 'pendidikan_akh_ket', 'jenis_pkrjn',
            'jenis_pkrjn_ket', 'gol_drh', 'stat_kwn_ket', 'tgl_kwn',
            'stat_hbkel_1', 'alamat', 'no_rt', 'no_rw', 'dusun', 'kode_pos',
            'telp', 'no_prop', 'nama_prop', 'no_kab', 'nama_kab', 'no_kec',
            'nama_kec', 'no_kel', 'nama_kel', 'no_kk'
        ]
