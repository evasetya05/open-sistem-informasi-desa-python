from django.shortcuts import render
from .models import Header, Banner
# views.py
from django.shortcuts import render
from .models import Header, Banner

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


from django.shortcuts import render
from django.contrib.auth import get_user_model
from dashboard.models import Header, Banner

User = get_user_model()


def index(request):
    header = Header.objects.first()
    banners = Banner.objects.filter(is_active=True)  # kalau ada field aktif

    if request.user.is_authenticated:
        current_user = request.user

        if current_user.user_position == 'KD':  # Kepala Desa
            return render(request, 'kd-dashboard.html',
                          context={'header': header, 'banners': banners, 'user': current_user})

        elif current_user.user_position == 'SD':  # Sekretaris Desa
            return render(request, 'sd-dashboard.html',
                          context={'header': header, 'banners': banners, 'user': current_user})

        elif current_user.user_position == 'ST':  # Staff Desa
            return render(request, 'staff_desa-dashboard.html',
                          context={'header': header, 'banners': banners, 'user': current_user})

        elif current_user.user_position == 'RW':  # RW
            return render(request, 'rw-dashboard.html',
                          context={'header': header, 'banners': banners, 'user': current_user})

        elif current_user.user_position == 'RT':  # RT
            return render(request, 'rt-dashboard.html',
                          context={'header': header, 'banners': banners, 'user': current_user})

        else:
            # fallback untuk role lain (misalnya warga)
            return render(request, 'i-dashboard.html',
                          context={'header': header, 'banners': banners, 'user': current_user})

    # kalau user belum login
    return render(request, 'i-dashboard.html', context={'header': header, 'banners': banners})


def base(request):
    return render(request, 'partials/base.html')
