import requests
import json
import os
import sys
import django

# Настраиваем Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

def check_api():
    # Проверяем API напрямую через модуль requests
    url = "http://localhost:8000/api/v1/vehicles/"
    
    try:
        response = requests.get(url)
        print(f"Статус код: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print(f"Длина ответа: {len(str(data))} байт")
                print(f"Количество объектов: {data.get('count', 'Нет данных')}")
                print(f"Структура объекта: {json.dumps(data, indent=2, ensure_ascii=False)[:200]}...")
            except json.JSONDecodeError:
                print("Ошибка декодирования JSON")
                print(f"Содержимое ответа: {response.text[:100]}...")
        else:
            print(f"Ошибка запроса: {response.text[:100]}...")
    except Exception as e:
        print(f"Исключение при запросе: {e}")
        
    # Проверяем напрямую через Django
    from logistics.models import Vehicle
    print("\nПроверка через Django ORM:")
    vehicles = Vehicle.objects.all()
    print(f"Количество транспортных средств: {vehicles.count()}")
    if vehicles.count() > 0:
        for v in vehicles[:3]:  # Выводим первые 3 транспортных средства
            print(f"- {v.number} ({v.brand} {v.model}): {v.status}")

if __name__ == "__main__":
    check_api() 