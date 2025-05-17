#!/bin/bash

# Скрипт для сборки Android приложения

# Цвета для вывода сообщений
GREEN='\033[0;32m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}=== Начало сборки Android приложения ===${NC}"

# Устанавливаем переменные окружения
export ANDROID_HOME=$HOME/Library/Android/sdk
export PATH=$PATH:$ANDROID_HOME/tools:$ANDROID_HOME/platform-tools
export JAVA_HOME=/opt/homebrew/opt/openjdk@17/libexec/openjdk.jdk/Contents/Home
export PATH=$JAVA_HOME/bin:$PATH

# Проверяем версию Java
JAVA_VERSION=$(java -version 2>&1 | head -n 1)
echo -e "${BLUE}Using Java: $JAVA_VERSION${NC}"

# Проверяем, установлен ли Cordova
if ! command -v cordova &> /dev/null; then
    echo -e "${RED}Ошибка: Cordova не установлен. Установите его с помощью npm install -g cordova${NC}"
    exit 1
fi

# Проверяем существование платформы Android
if [ ! -d "platforms/android" ]; then
    echo -e "${BLUE}Добавление платформы Android...${NC}"
    cordova platform add android
fi

# Проверяем ресурсы
if [ ! -d "res/android" ]; then
    echo -e "${RED}Ошибка: Отсутствует директория с ресурсами res/android${NC}"
    exit 1
fi

# Сборка в режиме отладки
echo -e "${BLUE}Сборка отладочной версии приложения...${NC}"
cordova build android --debug

# Если сборка отладочной версии прошла успешно, то собираем релизную версию
if [ $? -eq 0 ]; then
    echo -e "${GREEN}Отладочная версия собрана успешно.${NC}"
    
    echo -e "${BLUE}Сборка релизной версии приложения...${NC}"
    cordova build android --release
    
    # Проверяем результат сборки релизной версии
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}Релизная версия собрана успешно.${NC}"
        echo -e "${BLUE}APK файлы находятся в директории:${NC}"
        echo -e "${GREEN}platforms/android/app/build/outputs/apk/debug/app-debug.apk${NC}"
        echo -e "${GREEN}platforms/android/app/build/outputs/apk/release/app-release-unsigned.apk${NC}"
        
        # Путь к отладочному APK
        DEBUG_APK="platforms/android/app/build/outputs/apk/debug/app-debug.apk"
        
        # Предлагаем установить приложение на подключенный телефон
        echo -e "${BLUE}Хотите установить отладочную версию на подключенное устройство? (y/n)${NC}"
        read -r answer
        if [ "$answer" = "y" ]; then
            echo -e "${BLUE}Установка приложения на устройство...${NC}"
            adb install -r "$DEBUG_APK"
            
            if [ $? -eq 0 ]; then
                echo -e "${GREEN}Приложение успешно установлено!${NC}"
            else
                echo -e "${RED}Ошибка установки приложения. Проверьте подключение устройства.${NC}"
            fi
        fi
        
    else
        echo -e "${RED}Ошибка при сборке релизной версии.${NC}"
    fi
else
    echo -e "${RED}Ошибка при сборке отладочной версии.${NC}"
fi

echo -e "${BLUE}=== Завершение сборки Android приложения ===${NC}" 
 