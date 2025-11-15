from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin
from django.urls import path, include

from apps.dashboard.urls import index
from apps.dashboard.views import base

urlpatterns = [
                path('base/', base),
                path('admin/', admin.site.urls),
                path('User/', include('account.urls'), name='user'),
                path('users/', include('user.urls')),  # tambahkan ini

                path('dashboard/', include('apps.dashboard.urls'), name="dashboard"),
              
                path('', index, name="index"),
                path('blog/', include('apps.blog.urls')),  # Tambahkan ini

           
                path('home', include('apps.home.urls')),  # gunakan nama app kamu di sini
                path('layanan/', include('apps.layanan.urls')),  # gunakan nama app kamu di sini
                path('ckeditor/', include('ckeditor_uploader.urls')),
                path('penduduk/', include('apps.kependudukan.urls')),
                path("survey/", include("apps.survey.urls")),
                path("aset/", include("apps.aset.urls")),

               
                



              ] 

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
