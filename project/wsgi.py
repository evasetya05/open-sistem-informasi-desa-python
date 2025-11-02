import os
from django.core.wsgi import get_wsgi_application

# Deteksi apakah server sedang dijalankan via LiteSpeed
server_software = os.getenv('SERVER_SOFTWARE', '').lower()

if 'litespeed' in server_software or 'lsws' in server_software:
    settings_module = 'project.settings.production'
else:
    settings_module = 'project.settings.development'

os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

application = get_wsgi_application()
