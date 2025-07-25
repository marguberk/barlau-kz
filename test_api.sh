#!/bin/bash

# Скрипт для тестирования API и проверки изображений сотрудников
echo "🧪 Тестирование API BARLAU.KZ..."

echo ""
echo "📊 Проверка локального API (localhost:8000):"
echo "----------------------------------------"

# Проверка локального API employees
local_status=$(curl -s -w "%{http_code}" http://localhost:8000/api/employees/ -o /dev/null)
if [ "$local_status" -eq 200 ]; then
    echo "✅ Локальный API employees: работает"
    
    # Подсчет URL изображений
    photo_count=$(curl -s http://localhost:8000/api/employees/ | grep -o '"photo":"http://localhost:8000/media/employee_photos/[^"]*"' | wc -l)
    echo "📸 Найдено фотографий с полными URL: $photo_count"
    
    # Подсчет ролей
    total_employees=$(curl -s http://localhost:8000/api/employees/ | grep -o '"role":"[^"]*"' | wc -l)
    superadmin_count=$(curl -s http://localhost:8000/api/employees/ | grep -o '"role":"SUPERADMIN"' | wc -l)
    echo "👥 Всего сотрудников: $total_employees"
    echo "🔒 SUPERADMIN сотрудников (должны быть скрыты): $superadmin_count"
    
    # Примеры URL фотографий
    echo ""
    echo "📷 Примеры URL фотографий:"
    curl -s http://localhost:8000/api/employees/ | grep -o '"photo":"http://localhost:8000/media/employee_photos/[^"]*"' | head -3
else
    echo "❌ Локальный API недоступен (статус: $local_status)"
fi

echo ""
echo "🌐 Проверка продакшн API (barlau.org):"
echo "----------------------------------------"

# Проверка продакшн API vehicles (публичный)
prod_status=$(curl -s -w "%{http_code}" https://barlau.org/api/vehicles/ -o /dev/null)
if [ "$prod_status" -eq 200 ]; then
    echo "✅ Продакшн API vehicles: работает"
    vehicle_count=$(curl -s https://barlau.org/api/vehicles/ | grep -o '"count":[0-9]*' | cut -d: -f2)
    echo "🚛 Количество грузовиков: $vehicle_count"
else
    echo "❌ Продакшн API недоступен (статус: $prod_status)"
fi

# Проверка продакшн API employees (требует авторизации)
emp_status=$(curl -s -w "%{http_code}" https://barlau.org/api/employees/ -o /dev/null)
echo "🔐 Продакшн API employees: статус $emp_status (403 - нормально, требует авторизации)"

echo ""
echo "📱 Проверка Flutter приложений:"
echo "--------------------------------"

# Проверка запущенных Flutter процессов
flutter_count=$(ps aux | grep -E "flutter.*run.*(emulator|iPhone)" | grep -v grep | wc -l)
echo "🔄 Запущено Flutter приложений: $flutter_count"

if [ "$flutter_count" -gt 0 ]; then
    echo "📱 Активные Flutter процессы:"
    ps aux | grep -E "flutter.*run.*(emulator|iPhone)" | grep -v grep | sed 's/.*flutter.*run -d /  /' | sed 's/ .*//'
fi

echo ""
echo "💡 Рекомендации:"
echo "----------------"
echo "1. Android приложение должно использовать fallback на localhost:8000 API"
echo "2. iOS приложение должно подключаться к https://barlau.org/api"
echo "3. Фотографии должны иметь полные URL вместо относительных путей"
echo "4. SUPERADMIN роли должны быть скрыты от обычных пользователей"

echo ""
echo "✅ Тестирование завершено!" 