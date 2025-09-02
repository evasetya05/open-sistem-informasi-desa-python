
from django.contrib import admin
from django.urls import include, path
from home.views import home
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # gunakan nama app kamu di sini
    path('layanan/', include('layanan.urls')),  # gunakan nama app kamu di sini
    path('accounts/', include('accounts.urls')),  # gunakan nama app kamu di sini
    path('dashboards/', include('dashboard.urls')),  # gunakan nama app kamu di sini
    path('ckeditor/', include('ckeditor_uploader.urls'))
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)