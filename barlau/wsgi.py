"""
WSGI config for barlau project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

# Добавляем путь к проекту в sys.path
path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

# Для локальной разработки используйте barlau.settings
# Для PythonAnywhere используйте barlau.pythonanywhere_settings
# Проверяем, работаем ли на PythonAnywhere
if 'PYTHONANYWHERE_DOMAIN' in os.environ:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.pythonanywhere_settings')
else:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')

application = get_wsgi_application()
