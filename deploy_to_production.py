#!/usr/bin/env python3
"""
Скрипт для деплоя локального Django на продакшн сервер
"""

import os
import subprocess
import tarfile
from pathlib import Path

# Настройки продакшн сервера
PRODUCTION_HOST = '85.202.192.33'
PRODUCTION_USER = 'ubuntu'
PRODUCTION_PASSWORD = '33q97KKRfmnHTY6dCiyuA3g='
PRODUCTION_PATH = '/var/www/barlau'

def run_ssh_command(command, description):
    """Выполняет команду через SSH на продакшн сервере"""
    print(f"🔧 {description}...")
    
    ssh_command = [
        'sshpass', '-p', PRODUCTION_PASSWORD,
        'ssh', '-o', 'StrictHostKeyChecking=no',
        f'{PRODUCTION_USER}@{PRODUCTION_HOST}',
        command
    ]
    
    try:
        result = subprocess.run(ssh_command, capture_output=True, text=True, timeout=60)
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            return result.stdout
        else:
            print(f"❌ {description} - ошибка: {result.stderr}")
            return None
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return None

def run_scp_command(local_path, remote_path, description):
    """Копирует файл на продакшн сервер"""
    print(f"📁 {description}...")
    
    scp_command = [
        'sshpass', '-p', PRODUCTION_PASSWORD,
        'scp', '-o', 'StrictHostKeyChecking=no',
        local_path, f'{PRODUCTION_USER}@{PRODUCTION_HOST}:{remote_path}'
    ]
    
    try:
        result = subprocess.run(scp_command, capture_output=True, text=True, timeout=120)
        if result.returncode == 0:
            print(f"✅ {description} - успешно")
            return True
        else:
            print(f"❌ {description} - ошибка: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} - исключение: {e}")
        return False

def create_archive(files_to_archive, archive_name, description):
    """Создает архив с файлами"""
    print(f"📦 {description}...")
    
    try:
        with tarfile.open(archive_name, 'w:gz') as tar:
            for file_path in files_to_archive:
                if os.path.exists(file_path):
                    tar.add(file_path, arcname=file_path)
                    print(f"  📄 Добавлен: {file_path}")
                else:
                    print(f"  ⚠️  Файл не найден: {file_path}")
        
        print(f"✅ {description} - успешно")
        return True
    except Exception as e:
        print(f"❌ {description} - ошибка: {e}")
        return False

def sync_migrations():
    """Синхронизирует миграции"""
    print("\n🔄 Синхронизация миграций...")
    
    migrations_files = [
        'core/migrations/',
        'logistics/migrations/',
        'accounts/migrations/'
    ]
    
    archive_name = "migrations.tar.gz"
    if create_archive(migrations_files, archive_name, "Создание архива миграций"):
        if run_scp_command(archive_name, f'{PRODUCTION_PATH}/', "Копирование миграций"):
            run_ssh_command(
                f'cd {PRODUCTION_PATH} && tar -xzf {archive_name} && rm {archive_name}',
                "Распаковка миграций на сервере"
            )
        os.remove(archive_name)

def sync_templates():
    """Синхронизирует шаблоны"""
    print("\n🔄 Синхронизация шаблонов...")
    
    templates_files = [
        'core/templates/',
        'logistics/templates/',
        'templates/'
    ]
    
    archive_name = "templates.tar.gz"
    if create_archive(templates_files, archive_name, "Создание архива шаблонов"):
        if run_scp_command(archive_name, f'{PRODUCTION_PATH}/', "Копирование шаблонов"):
            run_ssh_command(
                f'cd {PRODUCTION_PATH} && tar -xzf {archive_name} && rm {archive_name}',
                "Распаковка шаблонов на сервере"
            )
        os.remove(archive_name)

def sync_static_files():
    """Синхронизирует статические файлы"""
    print("\n🔄 Синхронизация статических файлов...")
    
    static_files = [
        'static/',
        'core/static/',
        'logistics/static/'
    ]
    
    archive_name = "static.tar.gz"
    if create_archive(static_files, archive_name, "Создание архива статических файлов"):
        if run_scp_command(archive_name, f'{PRODUCTION_PATH}/', "Копирование статических файлов"):
            run_ssh_command(
                f'cd {PRODUCTION_PATH} && tar -xzf {archive_name} && rm {archive_name}',
                "Распаковка статических файлов на сервере"
            )
        os.remove(archive_name)

def sync_python_files():
    """Синхронизирует Python файлы"""
    print("\n🔄 Синхронизация Python файлов...")
    
    python_files = [
        'core/models.py',
        'core/views.py',
        'core/admin.py',
        'core/api.py',
        'core/urls.py',
        'core/serializers.py',
        'logistics/models.py',
        'logistics/views/',
        'logistics/admin.py',
        'logistics/api.py',
        'logistics/urls.py',
        'logistics/serializers.py',
        'accounts/models.py',
        'accounts/views.py',
        'accounts/admin.py',
        'accounts/urls.py',
        'maro/settings.py',
        'maro/urls.py',
        'maro/wsgi.py',
    ]
    
    archive_name = "python_files.tar.gz"
    if create_archive(python_files, archive_name, "Создание архива Python файлов"):
        if run_scp_command(archive_name, f'{PRODUCTION_PATH}/', "Копирование Python файлов"):
            run_ssh_command(
                f'cd {PRODUCTION_PATH} && tar -xzf {archive_name} && rm {archive_name}',
                "Распаковка Python файлов на сервере"
            )
        os.remove(archive_name)

def apply_migrations():
    """Применяет миграции на продакшн сервере"""
    print("\n🔄 Применение миграций на продакшн сервере...")
    
    run_ssh_command(
        f'cd {PRODUCTION_PATH} && source venv/bin/activate && python manage.py migrate',
        "Применение миграций"
    )

def collect_static():
    """Собирает статические файлы на продакшн сервере"""
    print("\n🔄 Сбор статических файлов на продакшн сервере...")
    
    run_ssh_command(
        f'cd {PRODUCTION_PATH} && source venv/bin/activate && python manage.py collectstatic --noinput',
        "Сбор статических файлов"
    )

def restart_services():
    """Перезапускает сервисы на продакшн сервере"""
    print("\n🔄 Перезапуск сервисов на продакшн сервере...")
    
    run_ssh_command(
        'sudo systemctl restart gunicorn',
        "Перезапуск Gunicorn"
    )
    
    run_ssh_command(
        'sudo systemctl restart nginx',
        "Перезапуск Nginx"
    )

def main():
    """Основная функция деплоя"""
    print("🚀 Начинаем деплой на продакшн сервер...")
    print(f"📍 Сервер: {PRODUCTION_HOST}")
    print(f"👤 Пользователь: {PRODUCTION_USER}")
    print(f"📁 Путь: {PRODUCTION_PATH}")
    
    # Проверяем подключение к серверу
    if not run_ssh_command('echo "Подключение успешно"', "Проверка подключения к серверу"):
        print("❌ Не удалось подключиться к серверу")
        return
    
    # Синхронизируем файлы
    sync_migrations()
    sync_templates()
    sync_static_files()
    sync_python_files()
    
    # Применяем изменения на сервере
    apply_migrations()
    collect_static()
    restart_services()
    
    print("\n✅ Деплой завершен!")
    print("🌐 Продакшн сервер: https://barlau.org")

if __name__ == '__main__':
    main() 