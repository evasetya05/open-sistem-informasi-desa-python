
from django.shortcuts import render
from .models import Header, Banner
from apps.survey.models import Survey, Response
from django.contrib.auth import get_user_model
from apps.kependudukan.models import Penduduk, KartuKeluarga
import datetime

User = get_user_model()


def dashboard(request):
    header = Header.objects.first()  # kalau kosong akan None
    banners = Banner.objects.filter(is_active=True)  # kalau kosong akan []
    
    return render(
        request,
        "dashboard.html",
        {
            "header": header,
            "banners": banners,
        }
    )




def index(request):
    header = Header.objects.first()
    banners = Banner.objects.filter(is_active=True)

    # statistik dasar kependudukan untuk semua pengguna
    qs_hidup = Penduduk.objects.filter(status_hidup=True)
    total_penduduk = Penduduk.objects.count()
    total_penduduk_hidup = qs_hidup.count()
    total_penduduk_meninggal = Penduduk.objects.filter(status_hidup=False).count()
    total_kk = KartuKeluarga.objects.count()
    # gunakan keterangan jenis kelamin: Lk = laki-laki, Pr = perempuan
    total_laki = qs_hidup.filter(jenis_klmin_ket__iexact='Lk').count()
    total_perempuan = qs_hidup.filter(jenis_klmin_ket__iexact='Pr').count()
    dusun_count = qs_hidup.exclude(dusun__isnull=True).exclude(dusun__exact='').values('dusun').distinct().count()
    rt_count = qs_hidup.exclude(no_rt__isnull=True).exclude(no_rt__exact='').values('no_rt').distinct().count()

    if request.user.is_authenticated:
        current_user = request.user

        # Ambil semua survey
        surveys = Survey.objects.all()

        # Buat dict survey_id -> response user
        user_responses = {}
        for survey in surveys:
            resp = survey.responses.filter(respondent=current_user).first()
            user_responses[survey.id] = resp

        # distribusi umur per 5 tahun untuk penduduk hidup
        today = datetime.date.today()
        kelompok = {}
        for tgl in qs_hidup.values_list('tgl_lhr', flat=True):
            if not tgl:
                continue
            umur = today.year - tgl.year - ((today.month, today.day) < (tgl.month, tgl.day))
            if umur < 0:
                continue
            if umur >= 80:
                label = '80+'
            else:
                start = (umur // 5) * 5
                end = start + 4
                label = f"{start}-{end}"
            kelompok[label] = kelompok.get(label, 0) + 1

        # urutkan label umur secara numerik sederhana (0-4,5-9,...,80+)
        def sort_key(l):
            if l.endswith('+'):
                return 10_000
            return int(l.split('-')[0])

        age_labels = sorted(kelompok.keys(), key=sort_key)
        age_counts = [kelompok[k] for k in age_labels]

        # distribusi pendidikan, agama, pekerjaan untuk penduduk hidup
        def build_dist(queryset, field):
            counts = {}
            for value in queryset.values_list(field, flat=True):
                if not value:
                    continue
                value = value.strip()
                if not value:
                    continue
                counts[value] = counts.get(value, 0) + 1
            labels = sorted(counts.keys())
            data = [counts[k] for k in labels]
            return labels, data

        edu_labels, edu_counts = build_dist(qs_hidup, 'pendidikan_akh_ket')
        agama_labels, agama_counts = build_dist(qs_hidup, 'agama_ket')
        kerja_labels, kerja_counts = build_dist(qs_hidup, 'jenis_pkrjn_ket')

        context = {
            'header': header,
            'banners': banners,
            'user': current_user,
            'surveys': surveys,
            'user_responses': user_responses,
            'total_penduduk': total_penduduk,
            'total_penduduk_hidup': total_penduduk_hidup,
            'total_penduduk_meninggal': total_penduduk_meninggal,
            'total_kk': total_kk,
            'total_laki': total_laki,
            'total_perempuan': total_perempuan,
            'dusun_count': dusun_count,
            'rt_count': rt_count,
            'age_labels': age_labels,
            'age_counts': age_counts,
            'edu_labels': edu_labels,
            'edu_counts': edu_counts,
            'agama_labels': agama_labels,
            'agama_counts': agama_counts,
            'kerja_labels': kerja_labels,
            'kerja_counts': kerja_counts,
        }

        if current_user.user_position == 'KD':
            return render(request, 'kd-dashboard.html', context)
        elif current_user.user_position == 'SD':
            return render(request, 'sd-dashboard.html', context)
        elif current_user.user_position == 'ST':
            return render(request, 'staff_desa-dashboard.html', context)
        elif current_user.user_position == 'RW':
            return render(request, 'rw-dashboard.html', context)
        elif current_user.user_position == 'RT':
            return render(request, 'rt-dashboard.html', context)
        else:
            return render(request, 'i-dashboard.html', context)

    # user belum login: tampilkan i-dashboard dengan statistik dasar desa
    public_context = {
        'header': header,
        'banners': banners,
        'total_penduduk': total_penduduk,
        'total_penduduk_hidup': total_penduduk_hidup,
        'total_penduduk_meninggal': total_penduduk_meninggal,
        'total_kk': total_kk,
        'total_laki': total_laki,
        'total_perempuan': total_perempuan,
        'dusun_count': dusun_count,
        'rt_count': rt_count,
    }
    return render(request, 'i-dashboard.html', context=public_context)


def base(request):
    return render(request, 'partials/base.html')
