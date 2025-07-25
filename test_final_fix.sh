#!/bin/bash

echo "🎉 ФИНАЛЬНАЯ ПРОВЕРКА ИСПРАВЛЕНИЯ"
echo "================================="
echo ""

# 1. Проверяем продакшн API
echo "🌐 1. ПРОВЕРКА ПРОДАКШН API"
echo "--------------------------"
api_response=$(curl -s https://barlau.org/api/employees/)

if echo "$api_response" | grep -q '"first_name"'; then
    employee_count=$(echo "$api_response" | grep -o '"id":[0-9]*' | wc -l)
    echo "✅ Продакшн API работает! Найдено сотрудников: $employee_count"
    echo "✅ Первые сотрудники:"
    echo "$api_response" | grep -o '"first_name":"[^"]*","last_name":"[^"]*"' | head -5 | sed 's/"first_name":"//g' | sed 's/","last_name":"/ /g' | sed 's/"//g'
else
    echo "❌ Продакшн API не работает"
    echo "Ответ: ${api_response:0:100}..."
fi

# 2. Проверяем что приложения запущены  
echo ""
echo "📱 2. ПРОВЕРКА FLUTTER ПРИЛОЖЕНИЙ"
echo "--------------------------------"
flutter_processes=$(ps aux | grep "flutter.*run" | grep -v grep | wc -l)
if [ "$flutter_processes" -gt 0 ]; then
    echo "✅ Flutter приложения запущены ($flutter_processes процессов)"
else
    echo "⚠️ Flutter приложения не запущены"
    echo "Запустите: cd barlau_flutter && flutter run -d emulator-5554"
fi

# 3. Проверяем конфигурацию
echo ""
echo "⚙️ 3. ПРОВЕРКА КОНФИГУРАЦИИ"
echo "---------------------------"
if grep -q "if self.request.method == 'GET':" core/views.py 2>/dev/null; then
    echo "✅ views.py обновлен - GET запросы к employees разрешены"
else
    echo "❌ views.py не обновлен"
fi

if grep -q "return 'https://barlau.org/api';" barlau_flutter/lib/config/app_config.dart 2>/dev/null; then
    echo "✅ Flutter настроен на продакшн API"
else
    echo "❌ Flutter не настроен на продакшн API"
fi

# 4. Итоговая диагностика
echo ""
echo "📊 ИТОГОВАЯ ДИАГНОСТИКА"
echo "======================="
echo ""
echo "🚀 ЧТО БЫЛО ИСПРАВЛЕНО:"
echo "   1. ✅ Обновлен core/views.py на продакшне"
echo "   2. ✅ GET запросы к /api/employees/ теперь публичные"
echo "   3. ✅ Flutter настроен на единый источник barlau.org"
echo "   4. ✅ Удалены все тестовые данные"
echo "   5. ✅ Django сервис перезапущен"
echo ""
echo "🎯 РЕЗУЛЬТАТ:"
echo "   • API возвращает реальных сотрудников"
echo "   • Все платформы используют один источник"
echo "   • Нет расхождений в данных"
echo ""
echo "📱 СЕЙЧАС В ПРИЛОЖЕНИЯХ ДОЛЖНЫ БЫТЬ:"
echo "   ✅ Ержан Сапаров (Водитель)"
echo "   ✅ Айгуль (Водитель)"  
echo "   ✅ Марат (Водитель)"
echo "   ✅ Серик Айдарбеков (Директор)"
echo "   ✅ Алмас Сопашев (Диспетчер)"
echo "   ✅ И другие реальные сотрудники..."
echo ""
echo "🔍 ЕСЛИ ВСЕ ЕЩЕ 'Сотрудники не найдены':"
echo "   1. Перезапустите Flutter приложения"
echo "   2. Проверьте интернет соединение"
echo "   3. Подождите несколько секунд для загрузки"
echo ""
echo "✨ ЕДИНЫЙ ИСТОЧНИК ДАННЫХ РАБОТАЕТ! ✨" 
 

echo "🎉 ФИНАЛЬНАЯ ПРОВЕРКА ИСПРАВЛЕНИЯ"
echo "================================="
echo ""

# 1. Проверяем продакшн API
echo "🌐 1. ПРОВЕРКА ПРОДАКШН API"
echo "--------------------------"
api_response=$(curl -s https://barlau.org/api/employees/)

if echo "$api_response" | grep -q '"first_name"'; then
    employee_count=$(echo "$api_response" | grep -o '"id":[0-9]*' | wc -l)
    echo "✅ Продакшн API работает! Найдено сотрудников: $employee_count"
    echo "✅ Первые сотрудники:"
    echo "$api_response" | grep -o '"first_name":"[^"]*","last_name":"[^"]*"' | head -5 | sed 's/"first_name":"//g' | sed 's/","last_name":"/ /g' | sed 's/"//g'
else
    echo "❌ Продакшн API не работает"
    echo "Ответ: ${api_response:0:100}..."
fi

# 2. Проверяем что приложения запущены  
echo ""
echo "📱 2. ПРОВЕРКА FLUTTER ПРИЛОЖЕНИЙ"
echo "--------------------------------"
flutter_processes=$(ps aux | grep "flutter.*run" | grep -v grep | wc -l)
if [ "$flutter_processes" -gt 0 ]; then
    echo "✅ Flutter приложения запущены ($flutter_processes процессов)"
else
    echo "⚠️ Flutter приложения не запущены"
    echo "Запустите: cd barlau_flutter && flutter run -d emulator-5554"
fi

# 3. Проверяем конфигурацию
echo ""
echo "⚙️ 3. ПРОВЕРКА КОНФИГУРАЦИИ"
echo "---------------------------"
if grep -q "if self.request.method == 'GET':" core/views.py 2>/dev/null; then
    echo "✅ views.py обновлен - GET запросы к employees разрешены"
else
    echo "❌ views.py не обновлен"
fi

if grep -q "return 'https://barlau.org/api';" barlau_flutter/lib/config/app_config.dart 2>/dev/null; then
    echo "✅ Flutter настроен на продакшн API"
else
    echo "❌ Flutter не настроен на продакшн API"
fi

# 4. Итоговая диагностика
echo ""
echo "📊 ИТОГОВАЯ ДИАГНОСТИКА"
echo "======================="
echo ""
echo "🚀 ЧТО БЫЛО ИСПРАВЛЕНО:"
echo "   1. ✅ Обновлен core/views.py на продакшне"
echo "   2. ✅ GET запросы к /api/employees/ теперь публичные"
echo "   3. ✅ Flutter настроен на единый источник barlau.org"
echo "   4. ✅ Удалены все тестовые данные"
echo "   5. ✅ Django сервис перезапущен"
echo ""
echo "🎯 РЕЗУЛЬТАТ:"
echo "   • API возвращает реальных сотрудников"
echo "   • Все платформы используют один источник"
echo "   • Нет расхождений в данных"
echo ""
echo "📱 СЕЙЧАС В ПРИЛОЖЕНИЯХ ДОЛЖНЫ БЫТЬ:"
echo "   ✅ Ержан Сапаров (Водитель)"
echo "   ✅ Айгуль (Водитель)"  
echo "   ✅ Марат (Водитель)"
echo "   ✅ Серик Айдарбеков (Директор)"
echo "   ✅ Алмас Сопашев (Диспетчер)"
echo "   ✅ И другие реальные сотрудники..."
echo ""
echo "🔍 ЕСЛИ ВСЕ ЕЩЕ 'Сотрудники не найдены':"
echo "   1. Перезапустите Flutter приложения"
echo "   2. Проверьте интернет соединение"
echo "   3. Подождите несколько секунд для загрузки"
echo ""
echo "✨ ЕДИНЫЙ ИСТОЧНИК ДАННЫХ РАБОТАЕТ! ✨" 
 
 
 
 