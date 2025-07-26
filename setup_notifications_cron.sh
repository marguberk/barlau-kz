#!/bin/bash

# 🔔 Скрипт настройки cron задач для системы уведомлений BARLAU.KZ
# Автор: Система управления уведомлениями
# Дата: $(date +%Y-%m-%d)

echo "🔔 Настройка cron задач для системы уведомлений BARLAU.KZ"
echo "=================================================="

# Определение путей
PROJECT_PATH="/Users/almaty/cursors/maro"
VENV_PATH="$PROJECT_PATH/venv311"
PYTHON_PATH="$VENV_PATH/bin/python"
MANAGE_PY="$PROJECT_PATH/manage.py"

# Проверка существования путей
if [ ! -d "$PROJECT_PATH" ]; then
    echo "❌ Ошибка: Проект не найден по пути $PROJECT_PATH"
    exit 1
fi

if [ ! -d "$VENV_PATH" ]; then
    echo "❌ Ошибка: Виртуальное окружение не найдено по пути $VENV_PATH"
    exit 1
fi

if [ ! -f "$MANAGE_PY" ]; then
    echo "❌ Ошибка: manage.py не найден по пути $MANAGE_PY"
    exit 1
fi

echo "✅ Все пути проверены успешно"

# Создание команд для cron
DAILY_CHECK="0 9 * * * cd $PROJECT_PATH && source $VENV_PATH/bin/activate && $PYTHON_PATH $MANAGE_PY check_expiring_documents --verbose >> /var/log/barlau_notifications.log 2>&1"

HOURLY_CHECK="0 */6 * * * cd $PROJECT_PATH && source $VENV_PATH/bin/activate && $PYTHON_PATH $MANAGE_PY check_expiring_documents >> /var/log/barlau_notifications.log 2>&1"

WEEKLY_CLEANUP="0 2 * * 0 cd $PROJECT_PATH && source $VENV_PATH/bin/activate && $PYTHON_PATH $MANAGE_PY shell -c \"from core.models import Notification; from django.utils import timezone; from datetime import timedelta; Notification.objects.filter(read=True, created_at__lt=timezone.now() - timedelta(days=30)).delete(); print('Старые уведомления очищены')\" >> /var/log/barlau_notifications.log 2>&1"

# Создание файла crontab
CRON_FILE="/tmp/barlau_notifications_cron"

echo "# BARLAU.KZ - Система уведомлений" > $CRON_FILE
echo "# Создано: $(date)" >> $CRON_FILE
echo "" >> $CRON_FILE
echo "# Ежедневная проверка истекающих документов в 9:00" >> $CRON_FILE
echo "$DAILY_CHECK" >> $CRON_FILE
echo "" >> $CRON_FILE
echo "# Проверка каждые 6 часов" >> $CRON_FILE
echo "$HOURLY_CHECK" >> $CRON_FILE
echo "" >> $CRON_FILE
echo "# Еженедельная очистка старых уведомлений (воскресенье в 2:00)" >> $CRON_FILE
echo "$WEEKLY_CLEANUP" >> $CRON_FILE

echo "📄 Создан файл crontab: $CRON_FILE"
echo ""
echo "📋 Содержимое crontab:"
cat $CRON_FILE

# Функция для установки crontab
install_crontab() {
    echo ""
    echo "🔧 Установка cron задач..."
    
    # Резервная копия текущего crontab
    if crontab -l > /dev/null 2>&1; then
        echo "💾 Создание резервной копии текущего crontab..."
        crontab -l > /tmp/crontab_backup_$(date +%Y%m%d_%H%M%S)
        echo "✅ Резервная копия создана"
    fi
    
    # Установка новых задач
    crontab $CRON_FILE
    if [ $? -eq 0 ]; then
        echo "✅ Cron задачи установлены успешно!"
    else
        echo "❌ Ошибка при установке cron задач"
        return 1
    fi
    
    # Проверка установленных задач
    echo ""
    echo "📋 Установленные cron задачи:"
    crontab -l | grep -A 10 -B 2 "BARLAU"
}

# Создание лог файла
create_log_file() {
    LOG_FILE="/var/log/barlau_notifications.log"
    
    echo "📝 Создание лог файла $LOG_FILE..."
    
    if [ ! -f "$LOG_FILE" ]; then
        sudo touch "$LOG_FILE"
        sudo chmod 666 "$LOG_FILE"
        echo "✅ Лог файл создан"
    else
        echo "ℹ️  Лог файл уже существует"
    fi
}

# Тестирование команды
test_command() {
    echo ""
    echo "🧪 Тестирование команды проверки документов..."
    
    cd $PROJECT_PATH
    source $VENV_PATH/bin/activate
    
    echo "Выполнение: python manage.py check_expiring_documents --verbose"
    $PYTHON_PATH $MANAGE_PY check_expiring_documents --verbose
    
    if [ $? -eq 0 ]; then
        echo "✅ Команда выполнена успешно!"
    else
        echo "❌ Ошибка при выполнении команды"
        return 1
    fi
}

# Меню выбора действий
echo ""
echo "Выберите действие:"
echo "1) Только создать файл crontab (не устанавливать)"
echo "2) Создать и установить cron задачи"
echo "3) Тестировать команду проверки документов"
echo "4) Создать лог файл"
echo "5) Выполнить всё (рекомендуется)"
echo "0) Выход"

read -p "Введите номер действия: " choice

case $choice in
    1)
        echo "✅ Файл crontab создан: $CRON_FILE"
        ;;
    2)
        install_crontab
        ;;
    3)
        test_command
        ;;
    4)
        create_log_file
        ;;
    5)
        create_log_file
        test_command
        if [ $? -eq 0 ]; then
            install_crontab
        else
            echo "❌ Тестирование не прошло, cron задачи не установлены"
        fi
        ;;
    0)
        echo "👋 Выход из скрипта"
        exit 0
        ;;
    *)
        echo "❌ Неверный выбор"
        exit 1
        ;;
esac

echo ""
echo "🎉 Настройка завершена!"
echo ""
echo "📚 Полезные команды:"
echo "  crontab -l                    # Просмотр текущих cron задач"
echo "  crontab -e                    # Редактирование cron задач"
echo "  tail -f /var/log/barlau_notifications.log  # Просмотр логов"
echo "  sudo service cron restart     # Перезапуск cron сервиса"
echo ""
echo "📖 Документация: NOTIFICATION_SYSTEM_GUIDE.md"
echo "🔗 Проект: $PROJECT_PATH" 