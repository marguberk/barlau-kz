#!/bin/bash

echo "🔐 ТЕСТ СЕССИОННОЙ АВТОРИЗАЦИИ DJANGO"
echo "====================================="
echo ""

# 1. Получаем CSRF токен и куки сессии
echo "1. Получение CSRF токена..."
csrf_response=$(curl -s -c cookies.txt https://barlau.org/accounts/login/)
csrf_token=$(echo "$csrf_response" | grep -o 'csrfmiddlewaretoken.*value="[^"]*"' | cut -d'"' -f2)

if [ -n "$csrf_token" ]; then
    echo "✅ CSRF токен получен: ${csrf_token:0:20}..."
    
    # 2. Логинимся через форму Django
    echo ""
    echo "2. Авторизация через Django форму..."
    login_response=$(curl -s -b cookies.txt -c cookies.txt -X POST https://barlau.org/accounts/login/ \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Referer: https://barlau.org/accounts/login/" \
      -d "csrfmiddlewaretoken=$csrf_token&username=admin&password=33q97KKRfmnHTY6dCiyuA3g=&next=/")
    
    if echo "$login_response" | grep -q "dashboard\|employees"; then
        echo "✅ Логин успешен!"
        
        # 3. Тестируем API с сессией
        echo ""
        echo "3. Тестирование API с сессией..."
        api_response=$(curl -s -b cookies.txt https://barlau.org/api/users/)
        
        if echo "$api_response" | grep -q '"username"'; then
            user_count=$(echo "$api_response" | grep -o '"id":[0-9]*' | wc -l)
            echo "✅ API с сессией работает! Найдено пользователей: $user_count"
        else
            echo "⚠️ API пользователей недоступен, пробуем другие endpoints"
            
            # Пробуем прямой доступ к данным
            profile_response=$(curl -s -b cookies.txt https://barlau.org/employees/)
            if echo "$profile_response" | grep -q "Серик\|Алмас\|Ерболат"; then
                echo "✅ Веб-интерфейс работает!"
                echo "✅ Сотрудники доступны через веб"
            fi
        fi
    else
        echo "❌ Логин не прошел"
        echo "Ответ: ${login_response:0:200}..."
    fi
else
    echo "❌ Не удалось получить CSRF токен"
fi

echo ""
echo "🎯 РЕШЕНИЕ ДЛЯ FLUTTER:"
echo "1. На продакшне не настроена API авторизация"
echo "2. Веб работает через сессии Django"
echo "3. Варианты решения:"
echo "   a) Настроить API авторизацию на продакшне"
echo "   b) Использовать веб-версию для просмотра сотрудников"
echo "   c) Временно отключить авторизацию для /api/employees/"
echo ""
echo "💡 БЫСТРОЕ РЕШЕНИЕ:"
echo "Временно сделать API /employees/ публичным для демонстрации" 
 

echo "🔐 ТЕСТ СЕССИОННОЙ АВТОРИЗАЦИИ DJANGO"
echo "====================================="
echo ""

# 1. Получаем CSRF токен и куки сессии
echo "1. Получение CSRF токена..."
csrf_response=$(curl -s -c cookies.txt https://barlau.org/accounts/login/)
csrf_token=$(echo "$csrf_response" | grep -o 'csrfmiddlewaretoken.*value="[^"]*"' | cut -d'"' -f2)

if [ -n "$csrf_token" ]; then
    echo "✅ CSRF токен получен: ${csrf_token:0:20}..."
    
    # 2. Логинимся через форму Django
    echo ""
    echo "2. Авторизация через Django форму..."
    login_response=$(curl -s -b cookies.txt -c cookies.txt -X POST https://barlau.org/accounts/login/ \
      -H "Content-Type: application/x-www-form-urlencoded" \
      -H "Referer: https://barlau.org/accounts/login/" \
      -d "csrfmiddlewaretoken=$csrf_token&username=admin&password=33q97KKRfmnHTY6dCiyuA3g=&next=/")
    
    if echo "$login_response" | grep -q "dashboard\|employees"; then
        echo "✅ Логин успешен!"
        
        # 3. Тестируем API с сессией
        echo ""
        echo "3. Тестирование API с сессией..."
        api_response=$(curl -s -b cookies.txt https://barlau.org/api/users/)
        
        if echo "$api_response" | grep -q '"username"'; then
            user_count=$(echo "$api_response" | grep -o '"id":[0-9]*' | wc -l)
            echo "✅ API с сессией работает! Найдено пользователей: $user_count"
        else
            echo "⚠️ API пользователей недоступен, пробуем другие endpoints"
            
            # Пробуем прямой доступ к данным
            profile_response=$(curl -s -b cookies.txt https://barlau.org/employees/)
            if echo "$profile_response" | grep -q "Серик\|Алмас\|Ерболат"; then
                echo "✅ Веб-интерфейс работает!"
                echo "✅ Сотрудники доступны через веб"
            fi
        fi
    else
        echo "❌ Логин не прошел"
        echo "Ответ: ${login_response:0:200}..."
    fi
else
    echo "❌ Не удалось получить CSRF токен"
fi

echo ""
echo "🎯 РЕШЕНИЕ ДЛЯ FLUTTER:"
echo "1. На продакшне не настроена API авторизация"
echo "2. Веб работает через сессии Django"
echo "3. Варианты решения:"
echo "   a) Настроить API авторизацию на продакшне"
echo "   b) Использовать веб-версию для просмотра сотрудников"
echo "   c) Временно отключить авторизацию для /api/employees/"
echo ""
echo "💡 БЫСТРОЕ РЕШЕНИЕ:"
echo "Временно сделать API /employees/ публичным для демонстрации" 
 
 
 
 