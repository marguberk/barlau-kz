#!/usr/bin/env python
import os
import sys
import django

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

# Импорт после настройки Django
from logistics.models import Vehicle

def main():
    vehicles = Vehicle.objects.all()
    print(f'Всего транспорта: {vehicles.count()}')
    
    if vehicles.count() > 0:
        print('Список транспорта:')
        for v in vehicles:
            driver_name = v.driver.get_full_name() if v.driver else 'Не назначен'
            print(f'- {v.number} ({v.brand} {v.model}), статус: {v.status}, водитель: {driver_name}')
    else:
        print('Транспорт не найден в базе данных')

if __name__ == '__main__':
    main() 