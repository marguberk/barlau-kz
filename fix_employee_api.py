#!/usr/bin/env python3
"""
Скрипт для исправления API сотрудников
"""
import os
import sys
import django

# Настройка Django
sys.path.append('/var/www/barlau')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

def fix_employee_api():
    """Исправление API сотрудников"""
    
    print("🔄 Исправление API сотрудников...")
    
    # Путь к файлу views.py
    views_path = '/var/www/barlau/core/views.py'
    
    # Читаем файл
    with open(views_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Заменяем строку
    old_line = "        queryset = User.objects.all().order_by('-date_joined', 'id')"
    new_line = "        queryset = User.objects.filter(is_active=True).order_by('-date_joined', 'id')"
    
    if old_line in content:
        content = content.replace(old_line, new_line)
        
        # Записываем обратно
        with open(views_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print("   ✅ API сотрудников исправлен - теперь возвращает только активных сотрудников")
    else:
        print("   ⚠️  Строка для замены не найдена")
    
    print(f"\n✅ Исправление API завершено!")

if __name__ == '__main__':
    try:
        fix_employee_api()
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1) 