#!/bin/bash

# Скрипт настройки VPS Ubuntu 24.04.2 LTS для Django проекта Barlau.kz

echo "=== Настройка VPS для Django проекта Barlau.kz ==="

# 1. Обновление системы
echo "1. Обновляем систему..."
sudo apt update && sudo apt upgrade -y

# 2. Установка Python и инструментов разработки
echo "2. Устанавливаем Python и инструменты разработки..."
sudo apt install -y python3-pip python3-venv python3-dev build-essential

# 3. Установка MySQL сервера и клиента
echo "3. Устанавливаем MySQL..."
sudo apt install -y mysql-server mysql-client libmysqlclient-dev

# 4. Установка Nginx веб-сервера
echo "4. Устанавливаем Nginx..."
sudo apt install -y nginx

# 5. Установка Git для клонирования репозитория
echo "5. Устанавливаем Git..."
sudo apt install -y git

# 6. Установка зависимостей для WeasyPrint и других библиотек
echo "6. Устанавливаем зависимости для PDF генерации..."
sudo apt install -y libcairo2-dev libpango1.0-dev libgdk-pixbuf2.0-dev libffi-dev shared-mime-info

# 7. Установка дополнительных инструментов
echo "7. Устанавливаем дополнительные инструменты..."
sudo apt install -y curl wget unzip htop nano

# 8. Создание пользователя для Django приложения
echo "8. Создаем пользователя для Django..."
sudo adduser --system --group --home /var/www/barlau barlau

# 9. Создание директорий для проекта
echo "9. Создаем директории для проекта..."
sudo mkdir -p /var/www/barlau
sudo mkdir -p /var/log/barlau
sudo chown -R barlau:barlau /var/www/barlau
sudo chown -R barlau:barlau /var/log/barlau

echo "=== Базовая настройка завершена! ==="
echo "Следующие шаги:"
echo "1. Настроить MySQL"
echo "2. Клонировать репозиторий"
echo "3. Создать виртуальное окружение"
echo "4. Установить зависимости Python"
echo "5. Настроить Nginx и Gunicorn" 