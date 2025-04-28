"""
WSGI config for barlau project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/howto/deployment/wsgi/
"""

import os
import sys

from django.core.wsgi import get_wsgi_application

# Добавьте путь к вашему проекту (раскомментируйте и замените на ваш путь на PythonAnywhere)
# path = '/home/yourusername/barlau-kz'
# if path not in sys.path:
#     sys.path.insert(0, path)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')

application = get_wsgi_application()
