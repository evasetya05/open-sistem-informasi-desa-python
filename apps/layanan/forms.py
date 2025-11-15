from django import forms
from .models import Antrian

class DaftarAntrianForm(forms.ModelForm):
    class Meta:
        model = Antrian
        fields = ['nik', 'nama', 'rt', 'rw']


