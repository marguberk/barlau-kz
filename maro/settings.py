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
    }
]
PWA_APP_ICONS_APPLE = [
    {
        'src': '/static/core/img/icons/icon-152x152.png',
        'sizes': '152x152'
    }
]
PWA_APP_SPLASH_SCREEN = [
    {
        'src': '/static/core/img/icons/icon-512x512.png',
        'media': '(device-width: 320px) and (device-height: 568px) and (-webkit-device-pixel-ratio: 2)'
    }
]
PWA_APP_DIR = 'ltr'
PWA_APP_LANG = 'ru-RU'
PWA_SERVICE_WORKER_PATH = os.path.join(BASE_DIR, 'static/core/js', 'service-worker.js') 