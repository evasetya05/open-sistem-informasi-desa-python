import pandas as pd
from datetime import datetime
from kependudukan.models import Penduduk  # ganti myapp sesuai nama app kamu

# Fungsi map gender
def map_gender(val):
    val = str(val).strip()
    if val in ['1', 'L', 'Lk', 'Laki-Laki']:
        return 'L'
    elif val in ['2', 'P', 'Pr', 'Perempuan']:
        return 'P'
    return None

# Fungsi parse tanggal
def parse_date(val):
    if pd.isna(val):
        return None
    if isinstance(val, datetime):
        return val.date()
    try:
        # Excel kadang format mm/dd/yyyy atau yyyy-mm-dd
        return pd.to_datetime(val).date()
    except:
        return None

# Load Excel
df = pd.read_excel('penduduk.xlsx')  # ganti path sesuai file Excel

# Loop dan simpan ke database
for _, row in df.iterrows():
    Penduduk.objects.create(
        no_kk=str(row['NO_KK']),
        nik=str(row['NIK']),
        nama_lgkp=row['NAMA_LGKP'],
        jenis_klmin=map_gender(row['JENIS_KLMIN']),
        jenis_klmin_ket=row.get('JENIS_KLMIN_KET', None),
        tmpt_lhr=row['TMPT_LHR'],
        tgl_lhr=parse_date(row['TGL_LHR']),
        agama=row.get('AGAMA', None),
        agama_ket=row.get('AGAMA_KET', ''),
        pddk_akh=row.get('PDDK_AKH', None),
        pendidikan_akh_ket=row.get('PENDIDIKAN_AKH_KET', ''),
        jenis_pkrjn=row.get('JENIS_PKRJN', None),
        jenis_pkrjn_ket=row.get('JENIS_PKRJN_KET', ''),
        gol_drh=row.get('GOL_DRH', None),
        stat_kwn_ket=row.get('STAT_KWN_KET', ''),
        tgl_kwn=parse_date(row.get('TGL_KWN')),
        stat_hbkel=row.get('STAT_HBKEL', None),
        stat_hbkel_1=row.get('STAT_HBKEL_1', ''),
        alamat=row.get('ALAMAT', ''),
        no_rt=row.get('NO_RT', ''),
        no_rw=row.get('NO_RW', ''),
        dusun=row.get('DUSUN', None),
        kode_pos=row.get('KODE_POS', None),
        telp=row.get('TELP', None),
        no_prop=row.get('NO_PROP', ''),
        nama_prop=row.get('NAMA_PROP', ''),
        no_kab=row.get('NO_KAB', ''),
        nama_kab=row.get('NAMA_KAB', ''),
        no_kec=row.get('NO_KEC', ''),
        nama_kec=row.get('NAMA_KEC', ''),
        no_kel=row.get('NO_KEL', ''),
        nama_kel=row.get('NAMA_KEL', '')
    )
