import os
from django.core.wsgi import get_wsgi_application

# Coba deteksi apakah dijalankan di server LiteSpeed
server_software = os.getenv('SERVER_SOFTWARE', '').lower()
is_litespeed = 'litespeed' in server_software or 'lsws' in server_software

if is_litespeed:
    settings_module = 'project.settings.production'
else:
    settings_module = 'project.settings.development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
