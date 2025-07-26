#!/bin/bash

echo "🔄 ОБНОВЛЕНИЕ НАВИГАЦИИ DJANGO ПОД FLUTTER"
echo "=========================================="
echo ""

# Файлы для обновления
templates=(
    "core/templates/core/dashboard.html"
    "core/templates/core/tasks.html" 
    "core/templates/core/employees.html"
    "core/templates/core/trucks.html"
    "core/templates/core/truck_detail.html"
    "core/templates/core/employee_detail.html"
    "core/templates/core/profile.html"
    "core/templates/core/notifications.html"
    "core/templates/core/checklist.html"
)

echo "📋 ПЛАН ИЗМЕНЕНИЙ:"
echo "1. Заменить 'Карта' → 'Заезды'"
echo "2. Обновить URL: core:map → core:trips"
echo "3. Изменить иконки: location.svg → truck.svg"
echo "4. Изменить мобильные иконки: mobile/location.svg → mobile/truck.svg"
echo ""

# Функция для замены в файле
update_template() {
    local file="$1"
    local filename=$(basename "$file")
    
    if [ ! -f "$file" ]; then
        echo "⚠️  Файл не найден: $file"
        return
    fi
    
    echo "🔧 Обновляем: $filename"
    
    # Создаем резервную копию
    cp "$file" "$file.backup"
    
    # Замены для десктопного меню в sidebar
    sed -i.tmp '
        # Замена URL карты на заезды
        s|href="{% url '\''core:map'\'' %}"|href="{% url '\''core:trips'\'' %}"|g
        
        # Замена текста "Карта" на "Заезды" в sidebar
        s|<div class="flex-1 justify-start text-gray-500 text-base font-medium leading-normal tracking-tight">Карта</div>|<div class="flex-1 justify-start text-gray-500 text-base font-medium leading-normal tracking-tight">Заезды</div>|g
        
        # Замена активного состояния текста "Карта" на "Заезды" 
        s|<div class="flex-1 text-blue-600 text-base font-medium leading-normal tracking-tight">Карта</div>|<div class="flex-1 text-blue-600 text-base font-medium leading-normal tracking-tight">Заезды</div>|g
        
        # Замена иконок location.svg на truck.svg для десктопа
        s|<img src="{% static '\''core/img/location.svg'\'' %}.*alt="Map"|<img src="{% static '\''core/img/truck.svg'\'' %}" alt="Trips"|g
        
        # Замена мобильных иконок
        s|<img src="{% static '\''core/img/mobile/location.svg'\'' %}" alt="Map"|<img src="{% static '\''core/img/mobile/truck.svg'\'' %}" alt="Trips"|g
        
        # Замена alt текста
        s|alt="Map"|alt="Trips"|g
        
        # Замена текста в мобильном меню
        s|<span class="text-xs text-\[9px\] mt-1 text-center whitespace-nowrap">Карта</span>|<span class="text-xs text-[9px] mt-1 text-center whitespace-nowrap">Заезды</span>|g
        s|<span class="text-xs text-\[10px\] mt-1">Карта</span>|<span class="text-xs text-[10px] mt-1">Заезды</span>|g
        s|<span class="text-xs mt-1">Карта</span>|<span class="text-xs mt-1">Заезды</span>|g
    ' "$file"
    
    # Удаляем временный файл
    rm -f "$file.tmp"
    
    echo "   ✅ Обновлен"
}

# Обновляем все шаблоны
for template in "${templates[@]}"; do
    update_template "$template"
done

echo ""
echo "🔧 СПЕЦИАЛЬНЫЕ ОБНОВЛЕНИЯ"
echo "========================="

# Обновление main_sections в dashboard.html для замены Карта → Заезды
echo "🔧 Обновляем main_sections в dashboard.html..."
if [ -f "core/templates/core/dashboard.html" ]; then
    sed -i.tmp "
        s|'name': 'Карта'|'name': 'Заезды'|g
        s|'url': '/map/'|'url': '/trips/'|g
    " "core/templates/core/dashboard.html"
    rm -f "core/templates/core/dashboard.html.tmp"
    echo "   ✅ main_sections обновлен"
fi

echo ""
echo "📊 РЕЗУЛЬТАТ ОБНОВЛЕНИЯ"
echo "======================"
echo ""

# Проверяем результаты
for template in "${templates[@]}"; do
    local filename=$(basename "$template")
    if [ -f "$template" ]; then
        trips_count=$(grep -c "core:trips" "$template" 2>/dev/null || echo "0")
        map_count=$(grep -c "core:map" "$template" 2>/dev/null || echo "0")
        echo "📄 $filename: Заезды=$trips_count, Карта=$map_count"
    fi
done

echo ""
echo "🎯 ИТОГ:"
echo "✅ Карта заменена на Заезды в навигации"
echo "✅ URL core:map → core:trips обновлены"
echo "✅ Иконки location.svg → truck.svg заменены"
echo "✅ Мобильные иконки обновлены"
echo ""
echo "🚀 Теперь Django веб интерфейс соответствует Flutter!"
echo "   Навигация: Главная → Задачи → Заезды → Грузовики → Сотрудники" 
 

echo "🔄 ОБНОВЛЕНИЕ НАВИГАЦИИ DJANGO ПОД FLUTTER"
echo "=========================================="
echo ""

# Файлы для обновления
templates=(
    "core/templates/core/dashboard.html"
    "core/templates/core/tasks.html" 
    "core/templates/core/employees.html"
    "core/templates/core/trucks.html"
    "core/templates/core/truck_detail.html"
    "core/templates/core/employee_detail.html"
    "core/templates/core/profile.html"
    "core/templates/core/notifications.html"
    "core/templates/core/checklist.html"
)

echo "📋 ПЛАН ИЗМЕНЕНИЙ:"
echo "1. Заменить 'Карта' → 'Заезды'"
echo "2. Обновить URL: core:map → core:trips"
echo "3. Изменить иконки: location.svg → truck.svg"
echo "4. Изменить мобильные иконки: mobile/location.svg → mobile/truck.svg"
echo ""

# Функция для замены в файле
update_template() {
    local file="$1"
    local filename=$(basename "$file")
    
    if [ ! -f "$file" ]; then
        echo "⚠️  Файл не найден: $file"
        return
    fi
    
    echo "🔧 Обновляем: $filename"
    
    # Создаем резервную копию
    cp "$file" "$file.backup"
    
    # Замены для десктопного меню в sidebar
    sed -i.tmp '
        # Замена URL карты на заезды
        s|href="{% url '\''core:map'\'' %}"|href="{% url '\''core:trips'\'' %}"|g
        
        # Замена текста "Карта" на "Заезды" в sidebar
        s|<div class="flex-1 justify-start text-gray-500 text-base font-medium leading-normal tracking-tight">Карта</div>|<div class="flex-1 justify-start text-gray-500 text-base font-medium leading-normal tracking-tight">Заезды</div>|g
        
        # Замена активного состояния текста "Карта" на "Заезды" 
        s|<div class="flex-1 text-blue-600 text-base font-medium leading-normal tracking-tight">Карта</div>|<div class="flex-1 text-blue-600 text-base font-medium leading-normal tracking-tight">Заезды</div>|g
        
        # Замена иконок location.svg на truck.svg для десктопа
        s|<img src="{% static '\''core/img/location.svg'\'' %}.*alt="Map"|<img src="{% static '\''core/img/truck.svg'\'' %}" alt="Trips"|g
        
        # Замена мобильных иконок
        s|<img src="{% static '\''core/img/mobile/location.svg'\'' %}" alt="Map"|<img src="{% static '\''core/img/mobile/truck.svg'\'' %}" alt="Trips"|g
        
        # Замена alt текста
        s|alt="Map"|alt="Trips"|g
        
        # Замена текста в мобильном меню
        s|<span class="text-xs text-\[9px\] mt-1 text-center whitespace-nowrap">Карта</span>|<span class="text-xs text-[9px] mt-1 text-center whitespace-nowrap">Заезды</span>|g
        s|<span class="text-xs text-\[10px\] mt-1">Карта</span>|<span class="text-xs text-[10px] mt-1">Заезды</span>|g
        s|<span class="text-xs mt-1">Карта</span>|<span class="text-xs mt-1">Заезды</span>|g
    ' "$file"
    
    # Удаляем временный файл
    rm -f "$file.tmp"
    
    echo "   ✅ Обновлен"
}

# Обновляем все шаблоны
for template in "${templates[@]}"; do
    update_template "$template"
done

echo ""
echo "🔧 СПЕЦИАЛЬНЫЕ ОБНОВЛЕНИЯ"
echo "========================="

# Обновление main_sections в dashboard.html для замены Карта → Заезды
echo "🔧 Обновляем main_sections в dashboard.html..."
if [ -f "core/templates/core/dashboard.html" ]; then
    sed -i.tmp "
        s|'name': 'Карта'|'name': 'Заезды'|g
        s|'url': '/map/'|'url': '/trips/'|g
    " "core/templates/core/dashboard.html"
    rm -f "core/templates/core/dashboard.html.tmp"
    echo "   ✅ main_sections обновлен"
fi

echo ""
echo "📊 РЕЗУЛЬТАТ ОБНОВЛЕНИЯ"
echo "======================"
echo ""

# Проверяем результаты
for template in "${templates[@]}"; do
    local filename=$(basename "$template")
    if [ -f "$template" ]; then
        trips_count=$(grep -c "core:trips" "$template" 2>/dev/null || echo "0")
        map_count=$(grep -c "core:map" "$template" 2>/dev/null || echo "0")
        echo "📄 $filename: Заезды=$trips_count, Карта=$map_count"
    fi
done

echo ""
echo "🎯 ИТОГ:"
echo "✅ Карта заменена на Заезды в навигации"
echo "✅ URL core:map → core:trips обновлены"
echo "✅ Иконки location.svg → truck.svg заменены"
echo "✅ Мобильные иконки обновлены"
echo ""
echo "🚀 Теперь Django веб интерфейс соответствует Flutter!"
echo "   Навигация: Главная → Задачи → Заезды → Грузовики → Сотрудники" 
 
 
 
 