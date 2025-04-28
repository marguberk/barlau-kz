"""
Django settings for barlau project on PythonAnywhere.
"""

from barlau.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['barguberk.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'barguberk$barlau',
        'USER': 'barguberk',
        'PASSWORD': 'barlau_db_password',
        'HOST': 'barguberk.mysql.pythonanywhere-services.com',
        'PORT': '',
    }
}

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Защита
SECURE_SSL_REDIRECT = False  # Установите в True, если есть SSL
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = False  # Установите в True, если есть SSL
CSRF_COOKIE_SECURE = False  # Установите в True, если есть SSL

# Настройки для медиа файлов
MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/yourusername/barlau-kz/media"

# Дополнительные настройки безопасности
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY" 