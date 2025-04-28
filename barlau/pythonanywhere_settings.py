"""
Django settings for barlau project on PythonAnywhere.
"""

from barlau.settings import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['barlaukz.pythonanywhere.com']

# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'barlaukz$barlau',
        'USER': 'barlaukz',
        'PASSWORD': 'barlau_db_password',
        'HOST': 'barlaukz.mysql.pythonanywhere-services.com',
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
MEDIA_ROOT = "/home/barlaukz/barlau-kz/media"

# Дополнительные настройки безопасности
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY" 