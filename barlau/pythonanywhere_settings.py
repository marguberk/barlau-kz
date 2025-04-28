from .settings import *

# PythonAnywhere настройки
DEBUG = False
ALLOWED_HOSTS = ["barlaukz.pythonanywhere.com"]

# Настройки базы данных для MySQL
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "barlaukz$barlau",
        "USER": "barlaukz",
        "PASSWORD": "barlauhQ217$#",
        "HOST": "barlaukz.mysql.pythonanywhere-services.com",
        "PORT": "",
    }
}

# Настройки для медиа файлов
MEDIA_URL = "/media/"
MEDIA_ROOT = "/home/barlaukz/barlau-kz/media"

# Настройки для статических файлов
STATIC_URL = "/static/"
STATIC_ROOT = "/home/barlaukz/barlau-kz/staticfiles"

# Дополнительные настройки безопасности
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = "DENY" 