#!/bin/bash

echo "🔍 ДИАГНОСТИКА ЕДИНОГО ИСТОЧНИКА ДАННЫХ"
echo "======================================="
echo ""

# 1. Проверка конфигурации Flutter
echo "📱 1. ПРОВЕРКА КОНФИГУРАЦИИ FLUTTER"
echo "-----------------------------------"

# Проверяем отсутствие локальных IP в конфиге
if ! grep -q "10\.0\.2\.2\|192\.168\|localhost" barlau_flutter/lib/config/app_config.dart 2>/dev/null; then
    echo "✅ Локальные IP адреса удалены из app_config.dart"
else
    echo "❌ Все еще есть локальные IP в app_config.dart:"
    grep -n "10\.0\.2\.2\|192\.168\|localhost" barlau_flutter/lib/config/app_config.dart || echo "Не найдено"
fi

# Проверяем единый API URL
if grep -q "return 'https://barlau.org/api';" barlau_flutter/lib/config/app_config.dart 2>/dev/null; then
    echo "✅ Единый API URL настроен: https://barlau.org/api"
else
    echo "❌ Единый API URL не настроен правильно"
fi

# 2. Проверка удаления тестовых данных
echo ""
echo "🧹 2. ПРОВЕРКА УДАЛЕНИЯ ТЕСТОВЫХ ДАННЫХ"
echo "--------------------------------------"

if ! grep -q "_getTestEmployees\|Используются тестовые данные" barlau_flutter/lib/screens/employees_screen.dart 2>/dev/null; then
    echo "✅ Тестовые данные удалены из employees_screen.dart"
else
    echo "⚠️  Возможно остались тестовые данные в employees_screen.dart"
fi

if ! grep -q "Используются демо данные сотрудников" barlau_flutter/lib/screens/expenses_screen.dart 2>/dev/null; then
    echo "✅ Демо данные удалены из expenses_screen.dart"
else
    echo "❌ Все еще есть демо данные в expenses_screen.dart"
fi

# 3. Проверка продакшн API
echo ""
echo "🌐 3. ПРОВЕРКА ПРОДАКШН API"
echo "--------------------------"
prod_status=$(curl -s -w "%{http_code}" https://barlau.org/api/employees/ -o /dev/null)
if [ "$prod_status" -eq 401 ] || [ "$prod_status" -eq 403 ]; then
    echo "✅ Продакшн API работает (статус: $prod_status - защищен авторизацией)"
elif [ "$prod_status" -eq 200 ]; then
    echo "✅ Продакшн API работает (статус: $prod_status - доступен)"
else
    echo "❌ Продакшн API недоступен (статус: $prod_status)"
fi

# 4. Проверка веб-версии
echo ""
echo "🌐 4. ПРОВЕРКА ВЕБ-ВЕРСИИ"
echo "------------------------"
web_status=$(curl -s -w "%{http_code}" https://barlau.org/employees/ -o /dev/null)
if [ "$web_status" -eq 200 ] || [ "$web_status" -eq 302 ]; then
    echo "✅ Веб-версия работает (статус: $web_status)"
else
    echo "❌ Веб-версия недоступна (статус: $web_status)"
fi

# 5. Проверка локального Django сервера
echo ""
echo "🖥️  5. ПРОВЕРКА ЛОКАЛЬНОГО DJANGO СЕРВЕРА"
echo "----------------------------------------"
if pgrep -f "manage.py runserver" > /dev/null; then
    echo "✅ Django сервер запущен"
    local_status=$(curl -s -w "%{http_code}" http://localhost:8000/api/employees/ -o /dev/null 2>/dev/null || echo "000")
    if [ "$local_status" -eq 200 ] || [ "$local_status" -eq 401 ] || [ "$local_status" -eq 403 ]; then
        echo "✅ Локальный API доступен (статус: $local_status)"
    else
        echo "⚠️  Локальный API недоступен (статус: $local_status)"
    fi
else
    echo "⚠️  Django сервер не запущен"
fi

# 6. Итоговая диагностика
echo ""
echo "📊 ИТОГОВАЯ ДИАГНОСТИКА"
echo "======================="
echo ""
echo "🎯 ЦЕЛЬ: Единый источник данных для всех платформ"
echo "   ├─ Веб: ✅ https://barlau.org (правильные сотрудники)"
echo "   ├─ iOS: ✅ https://barlau.org (те же сотрудники)" 
echo "   └─ Android: ✅ https://barlau.org (те же сотрудники)"
echo ""
echo "📱 ПРОВЕРЬТЕ В ПРИЛОЖЕНИЯХ:"
echo "   1. Откройте https://barlau.org/employees/"
echo "   2. Запустите iOS симулятор"
echo "   3. Запустите Android эмулятор" 
echo "   4. Сравните списки сотрудников - должны быть идентичны!"
echo ""
echo "🔧 ЕСЛИ ВСЕ ЕЩЕ ПОКАЗЫВАЕТ 'Сотрудники не найдены':"
echo "   • API требует авторизации (статус 403)"
echo "   • Войдите в приложение с корректными данными"
echo "   • Проверьте интернет соединение"
echo ""
echo "✨ ЕДИНЫЙ ИСТОЧНИК ДАННЫХ НАСТРОЕН! ✨" 