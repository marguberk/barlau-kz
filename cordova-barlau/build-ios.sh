#!/bin/bash

# Скрипт для сборки iOS приложения

# Цвета для вывода сообщений
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Начало сборки iOS приложения ===${NC}"

# Проверяем, установлен ли Cordova
if ! command -v cordova &> /dev/null; then
    echo -e "${RED}Ошибка: Cordova не установлен. Установите его с помощью npm install -g cordova${NC}"
    exit 1
fi

# Проверяем существование платформы iOS
if [ ! -d "platforms/ios" ]; then
    echo -e "${BLUE}Добавление платформы iOS...${NC}"
    cordova platform add ios
fi

# Проверяем ресурсы
if [ ! -d "res/ios" ]; then
    echo -e "${RED}Ошибка: Отсутствует директория с ресурсами res/ios${NC}"
    exit 1
fi

# Создаем директорию для иконок, если ее нет
if [ ! -d "platforms/ios/BARLAU.KZ/Images.xcassets/AppIcon.appiconset" ]; then
    echo -e "${BLUE}Создание директории для иконок...${NC}"
    mkdir -p "platforms/ios/BARLAU.KZ/Images.xcassets/AppIcon.appiconset"
fi

# Копируем иконки
echo -e "${BLUE}Копирование иконок...${NC}"
cp -r res/ios/*.png platforms/ios/BARLAU.KZ/Images.xcassets/AppIcon.appiconset/

# Запуск процесса сборки
echo -e "${BLUE}Сборка iOS приложения...${NC}"
cordova build ios

# Проверяем результат сборки
if [ $? -eq 0 ]; then
    echo -e "${GREEN}iOS приложение собрано успешно.${NC}"
    echo -e "${BLUE}Вы можете открыть проект в Xcode:${NC}"
    echo -e "${GREEN}open platforms/ios/BARLAU.KZ.xcworkspace${NC}"
    
    # Предлагаем открыть проект в Xcode
    echo -e "${BLUE}Хотите открыть проект в Xcode? (y/n)${NC}"
    read -r answer
    if [ "$answer" = "y" ]; then
        echo -e "${BLUE}Открытие проекта в Xcode...${NC}"
        open platforms/ios/BARLAU.KZ.xcworkspace
    fi
else
    echo -e "${RED}Ошибка при сборке iOS приложения.${NC}"
fi

echo -e "${BLUE}=== Завершение сборки iOS приложения ===${NC}" 
 