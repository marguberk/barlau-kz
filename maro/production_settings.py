import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-your-secret-key-here'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Custom user model
AUTH_USER_MODEL = 'accounts.User'

# Media files
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# File upload settings
FILE_UPLOAD_MAX_MEMORY_SIZE = 10 * 1024 * 1024  # 10MB
FILE_UPLOAD_PERMISSIONS = 0o644
FILE_UPLOAD_DIRECTORY_PERMISSIONS = 0o755

# Allowed file types
ALLOWED_DOCUMENT_TYPES = [
    'application/pdf',
    'application/msword',
    'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
]

ALLOWED_IMAGE_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
]

# Maximum file size (in bytes)
MAX_UPLOAD_SIZE = 10 * 1024 * 1024  # 10MB

# Database - используем продакшн базу
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'barlau_db',
        'USER': 'barlau_user',
        'PASSWORD': 'barlau_password',
        'HOST': '85.202.192.33',
        'PORT': '5432',
    }
}

# Добавляем 'pwa' в INSTALLED_APPS
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'accounts',
    'core',
    'logistics',
    'rest_framework',
    'phonenumber_field',
    'django_filters',
    'corsheaders',
    'pwa',  # Добавляем приложение PWA
    'django_extensions',  # Для show_urls
]

# Настройки PWA
PWA_APP_NAME = 'BARLAU.KZ'
PWA_APP_DESCRIPTION = "Система управления логистикой и сотрудниками"
PWA_APP_THEME_COLOR = "#2563EB"
PWA_APP_BACKGROUND_COLOR = "#ffffff"
PWA_APP_DISPLAY = 'standalone'
PWA_APP_SCOPE = '/'
PWA_APP_ORIENTATION = 'portrait-primary'
PWA_APP_START_URL = '/'
PWA_APP_STATUS_BAR_COLOR = 'black-translucent'
PWA_APP_ICONS = [
    {
        'src': '/static/core/img/icons/icon-72x72.png',
        'sizes': '72x72'
    },
    {
        'src': '/static/core/img/icons/icon-96x96.png',
        'sizes': '96x96'
    },
    {
        'src': '/static/core/img/icons/icon-128x128.png',
        'sizes': '128x128'
    },
    {
        'src': '/static/core/img/icons/icon-144x144.png',
        'sizes': '144x144'
    },
    {
        'src': '/static/core/img/icons/icon-152x152.png',
        'sizes': '152x152'
    },
    {
        'src': '/static/core/img/icons/icon-192x192.png',
        'sizes': '192x192'
    },
    {
        'src': '/static/core/img/icons/icon-384x384.png',
        'sizes': '384x384'
    },
    {
        'src': '/static/core/img/icons/icon-512x512.png',
        'sizes': '512x512'
    },
]

# Настройки REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
        'rest_framework.renderers.BrowsableAPIRenderer',
    ],
}

# Настройки CORS
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# Настройки статических файлов
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# Настройки шаблонов
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# Настройки middleware
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Настройки WSGI
WSGI_APPLICATION = 'maro.wsgi.application'

# Настройки паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Настройки интернационализации
LANGUAGE_CODE = 'ru-ru'
TIME_ZONE = 'Asia/Almaty'
USE_I18N = True
USE_TZ = True

# Настройки статических файлов
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Настройки логирования
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

# Настройки сессий
SESSION_COOKIE_AGE = 86400  # 24 часа
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# Настройки безопасности
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Настройки API
API_BASE_URL = 'https://barlau.org/api'
API_TOKEN = 'demo_token_for_web'  # Токен для доступа к API 