"""
WSGI config for barlau project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Проверяем наличие файла с настройками для PythonAnywhere
try:
    from barlau import pythonanywhere_settings
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.pythonanywhere_settings')
    print("Используются настройки PythonAnywhere")
except ImportError:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
    print("Используются стандартные настройки")

application = get_wsgi_application()
