
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

    if request.user.is_authenticated:
        current_user = request.user

        # Ambil semua survey
        surveys = Survey.objects.all()

        # Buat dict survey_id -> response user
        user_responses = {}
        for survey in surveys:
            resp = survey.responses.filter(respondent=current_user).first()
            user_responses[survey.id] = resp

        total_penduduk = Penduduk.objects.count()
        total_penduduk_hidup = Penduduk.objects.filter(status_hidup=True).count()
        total_penduduk_meninggal = Penduduk.objects.filter(status_hidup=False).count()
        total_kk = KartuKeluarga.objects.count()
        # gunakan keterangan jenis kelamin: Lk = laki-laki, Pr = perempuan
        total_laki = Penduduk.objects.filter(jenis_klmin_ket__iexact='Lk', status_hidup=True).count()
        total_perempuan = Penduduk.objects.filter(jenis_klmin_ket__iexact='Pr', status_hidup=True).count()

        # distribusi umur sederhana untuk penduduk hidup
        today = datetime.date.today()
        kelompok = {
            '0-5': 0,
            '6-18': 0,
            '19-59': 0,
            '60+': 0,
        }
        for tgl in Penduduk.objects.filter(status_hidup=True).values_list('tgl_lhr', flat=True):
            if not tgl:
                continue
            umur = today.year - tgl.year - ((today.month, today.day) < (tgl.month, tgl.day))
            if umur <= 5:
                kelompok['0-5'] += 1
            elif umur <= 18:
                kelompok['6-18'] += 1
            elif umur <= 59:
                kelompok['19-59'] += 1
            else:
                kelompok['60+'] += 1

        age_labels = list(kelompok.keys())
        age_counts = [kelompok[k] for k in age_labels]

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
            'age_labels': age_labels,
            'age_counts': age_counts,
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

    # user belum login
    return render(request, 'i-dashboard.html', context={'header': header, 'banners': banners})


def base(request):
    return render(request, 'partials/base.html')
