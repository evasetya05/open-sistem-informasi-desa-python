import pandas as pd
from aset.models import Aset

# Ganti path sesuai file Excel kamu
file_path = "/home/eva/Documents/tanah.xlsx"

# Baca file Excel
df = pd.read_excel(file_path)

# Pastikan nama kolom konsisten (hapus spasi dan ubah jadi huruf kecil)
df.columns = [c.strip().replace(" ", "_").replace(".", "_").lower() for c in df.columns]

for _, row in df.iterrows():
    Aset.objects.create(
        jenis="Tanah",  # misalnya semua data ini jenis tanah
        nama=row.get("nama"),
        no_ktp=row.get("no_ktp"),
        alamat=row.get("alamat"),
        rt_rw=row.get("rt_rw"),
        desa=row.get("desa"),
        kecamatan=row.get("kecamatan"),
        pekerjaan=row.get("pekerjaan"),
        no_sppt=row.get("no_sppt"),
        no_c_petok=row.get("no_c_petok"),
        persil=row.get("persil"),
        kelas=row.get("kelas"),
        nama_c=row.get("nama_c"),
        luasc=row.get("luasc"),
        luas_mohon=row.get("luas_mohon"),
        luas_sppt=row.get("luas_sppt"),
        nib=row.get("nib"),
        utara=row.get("utara"),
        timur=row.get("timur"),
        selatan=row.get("selatan"),
        barat=row.get("barat"),
        nilai_taksiran=None,
        keterangan=None,
        pemilik_luar=False,
        tahun_data=2025
    )
