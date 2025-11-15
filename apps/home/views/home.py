from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from apps.home.models import PostingInvestasi

def home(request):
    context = {
        "page_title": "Desa Digital Sumberoto",
        "tagline": "Membangun Desa Cerdas dan Mandiri",
    }
    return render(request, "home/home.html", context)


