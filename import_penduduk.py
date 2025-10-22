

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings.production")

import django
django.setup()

import pandas as pd
from django.conf import settings
import django
django.setup()

from kependudukan.models import Penduduk, KartuKeluarga

# === BACA FILE EXCEL ===
df = pd.read_excel("penduduk.xlsx")

print(f"📄 Membaca {len(df)} baris dari penduduk.xlsx")

# === NORMALISASI KOLOM ===
df.columns = df.columns.str.lower()

# === HAPUS DATA LAMA KK (opsional) ===
# KartuKeluarga.objects.all().delete()

# === BUAT / COCOKKAN KARTU KELUARGA ===
kk_map = {}
for kk in df['no_kk'].dropna().unique():
    kk_obj, _ = KartuKeluarga.objects.get_or_create(no_kk=str(kk).strip())
    kk_map[str(kk).strip()] = kk_obj

# === IMPOR DATA PENDUDUK ===
# === IMPOR DATA PENDUDUK ===
batch = []
for _, row in df.iterrows():
    # konversi tanggal ke None kalau NaT atau bukan datetime
    def safe_date(value):
        if pd.isna(value):
            return None
        try:
            return pd.to_datetime(value).date()
        except Exception:
            return None

    no_kk = str(row.get('no_kk', '')).strip()
    kk_obj = kk_map.get(no_kk)

    p = Penduduk(
        no_kk=kk_obj,
        nik=str(row.get('nik', '')).strip(),
        nama_lgkp=row.get('nama_lgkp', ''),
        jenis_klmin=row.get('jenis_klmin', ''),
        jenis_klmin_ket=row.get('jenis_klmin_ket', ''),
        tmpt_lhr=row.get('tmpt_lhr', ''),
        tgl_lhr=safe_date(row.get('tgl_lhr')),
        agama=row.get('agama', ''),
        agama_ket=row.get('agama_ket', ''),
        pddk_akh=row.get('pddk_akh', ''),
        pendidikan_akh_ket=row.get('pendidikan_akh_ket', ''),
        jenis_pkrjn=row.get('jenis_pkrjn', ''),
        jenis_pkrjn_ket=row.get('jenis_pkrjn_ket', ''),
        gol_drh=row.get('gol_drh', ''),
        stat_kwn_ket=row.get('stat_kwn_ket', ''),
        tgl_kwn=safe_date(row.get('tgl_kwn')),
        stat_hbkel=row.get('stat_hbkel', ''),
        stat_hbkel_1=row.get('stat_hbkel_1', ''),
        alamat=row.get('alamat', ''),
        no_rt=row.get('no_rt', ''),
        no_rw=row.get('no_rw', ''),
        dusun=row.get('dusun', ''),
        kode_pos=row.get('kode_pos', ''),
        telp=row.get('telp', ''),
        no_prop=row.get('no_prop', ''),
        nama_prop=row.get('nama_prop', ''),
        no_kab=row.get('no_kab', ''),
        nama_kab=row.get('nama_kab', ''),
        no_kec=row.get('no_kec', ''),
        nama_kec=row.get('nama_kec', ''),
        no_kel=row.get('no_kel', ''),
        nama_kel=row.get('nama_kel', ''),
    )
    batch.append(p)

Penduduk.objects.bulk_create(batch, batch_size=500)
print(f"✅ Selesai! {len(batch)} data penduduk berhasil diimpor.")
