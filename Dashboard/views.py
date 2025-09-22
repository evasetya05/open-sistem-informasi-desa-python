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
