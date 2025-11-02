"""HRManagement URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from dashboard.urls import index
from dashboard.views import base

urlpatterns = [
                path('base/', base),
                path('admin/', admin.site.urls),
                path('User/', include('account.urls'), name='user'),
                path('users/', include('user.urls')),  # tambahkan ini

                path('dashboard/', include('dashboard.urls'), name="dashboard"),
              
                path('', index, name="index"),
                path('blog/', include('blog.urls')),  # Tambahkan ini

           
                path('home', include('home.urls')),  # gunakan nama app kamu di sini
                path('layanan/', include('layanan.urls')),  # gunakan nama app kamu di sini
                path('ckeditor/', include('ckeditor_uploader.urls')),
                path('penduduk/', include('kependudukan.urls')),
                path("survey/", include("survey.urls")),
                path("aset/", include("aset.urls")),

               
                



              ] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
