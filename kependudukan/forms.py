from django import forms
from .models import Penduduk, KartuKeluarga


class KartuKeluargaForm(forms.ModelForm):
    class Meta:
        model = KartuKeluarga
        fields = ['no_kk', 'alamat', 'no_rt', 'no_rw', 'dusun', 'kode_pos']


class PendudukForm(forms.ModelForm):
    class Meta:
        model = Penduduk
        fields = [
            'nik', 'nama_lgkp', 'jenis_klmin', 'jenis_klmin_ket', 'tmpt_lhr', 'tgl_lhr',
            'agama', 'agama_ket', 'pddk_akh', 'pendidikan_akh_ket', 'jenis_pkrjn',
            'jenis_pkrjn_ket', 'gol_drh', 'stat_kwn_ket', 'tgl_kwn',
            'stat_hbkel_1', 'alamat', 'no_rt', 'no_rw', 'dusun', 'kode_pos',
            'telp', 'no_prop', 'nama_prop', 'no_kab', 'nama_kab', 'no_kec',
            'nama_kec', 'no_kel', 'nama_kel', 'no_kk', 'kk'
        ]
