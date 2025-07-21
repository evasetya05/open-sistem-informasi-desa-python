import os
import sys
import django

# Tambahkan path ke folder yang berisi 'sistem_desa'
sys.path.append('/home/spoonful/sumberoto/sistem_desa')  # GANTI jika path Anda berbeda

# Set environment Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sistem_desa.settings')

# Setup Django
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

# Ganti dengan data Anda
USERNAME = 'admin'
EMAIL = 'admin@example.com'
PASSWORD = 'admin123'

# Cek apakah user sudah ada
if not User.objects.filter(username=USERNAME).exists():
    User.objects.create_superuser(USERNAME, EMAIL, PASSWORD)
    print("✅ Superuser berhasil dibuat.")
else:
    print("⚠️ Superuser dengan username ini sudah ada.")
