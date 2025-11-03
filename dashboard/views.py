
from django.shortcuts import render
from .models import Header, Banner
from survey.models import Survey, Response
from django.contrib.auth import get_user_model

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

        context = {
            'header': header,
            'banners': banners,
            'user': current_user,
            'surveys': surveys,
            'user_responses': user_responses,
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
