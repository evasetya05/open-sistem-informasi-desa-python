from .base import *
import pymysql

DEBUG = False

ALLOWED_HOSTS = ['sumberoto.teknusa.com', 'www.sumberoto.teknusa.com']


pymysql.install_as_MySQLdb()

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'teknusas__desa_sumberoto',
        'USER': 'teknusas_desa_sumberoto',
        'PASSWORD': '@Pontianak123',
        'HOST': 'localhost',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
            'charset': 'utf8mb4',
        },
    }
}

STATIC_URL = '/static/'
STATIC_ROOT = '/home/teknusas/sumberoto.teknusa.com/static'

MEDIA_URL = '/media/'
MEDIA_ROOT = '/home/teknusas/sumberoto.teknusa.com/media'


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = ''
EMAIL_USE_TLS = False
EMAIL_PORT = ''
EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

