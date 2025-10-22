from django import forms
from .models import Aset

class AsetForm(forms.ModelForm):
    class Meta:
        model = Aset
        fields = "__all__"
        widgets = {
            "keterangan": forms.Textarea(attrs={"rows": 3}),
            "jenis": forms.Select(attrs={"class": "form-select"}),
            "sub_kategori": forms.TextInput(attrs={"placeholder": "contoh: sawah, rumah, motor"}),
        }
