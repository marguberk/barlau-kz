#!/bin/bash

# Скрипт настройки MySQL для Django проекта Barlau.kz

echo "=== Настройка MySQL для проекта Barlau.kz ==="

# 1. Запуск и включение MySQL
echo "1. Запускаем MySQL сервис..."
sudo systemctl start mysql
sudo systemctl enable mysql

# 2. Безопасная настройка MySQL
echo "2. Настраиваем безопасность MySQL..."
echo "ВАЖНО: Запомните root пароль для MySQL!"
sudo mysql_secure_installation

# 3. Создание базы данных и пользователя
echo "3. Создаем базу данных и пользователя..."
echo "Введите root пароль MySQL когда будет запрошен"

# Создаем SQL скрипт
cat > /tmp/create_db.sql << EOF
CREATE DATABASE barlau_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER 'barlau_user'@'localhost' IDENTIFIED BY 'BarlauSecure2024!';
GRANT ALL PRIVILEGES ON barlau_db.* TO 'barlau_user'@'localhost';
FLUSH PRIVILEGES;
SHOW DATABASES;
EOF

# Выполняем SQL скрипт
sudo mysql -u root -p < /tmp/create_db.sql

# Удаляем временный файл
rm /tmp/create_db.sql

echo "=== MySQL настроен! ==="
echo "База данных: barlau_db"
echo "Пользователь: barlau_user"
echo "Пароль: BarlauSecure2024!"
echo ""
echo "Добавьте эти данные в файл .env на сервере:"
echo "DB_NAME=barlau_db"
echo "DB_USER=barlau_user"
echo "DB_PASSWORD=BarlauSecure2024!"
echo "DB_HOST=localhost"
echo "DB_PORT=3306" 