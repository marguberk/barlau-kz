# Инструкция по развертыванию исправлений уведомлений на barlau.org

## Проблема
На продакшн сервере barlau.org не работают уведомления из-за того, что API требует аутентификации, а на продакшн DEBUG=False.

## Исправления
1. Добавлен `PublicNotificationViewSet` - публичный API для уведомлений без аутентификации
2. Обновлена логика фронтенда - сначала пытается использовать основной API, при ошибке переключается на публичный
3. Улучшена обработка ошибок в интерфейсе

## Команды для развертывания на сервере

### 1. Подключение к серверу
```bash
ssh root@barlau.org
# Пароль: 33q97KKRfmnHTY6dCiyuA3g=
```

### 2. Обновление кода
```bash
cd /home/barlau/barlau-kz
systemctl stop barlau
sudo -u barlau git pull origin local-version
```

### 3. Активация виртуального окружения и обновление
```bash
sudo -u barlau bash -c "source venv/bin/activate && python manage.py migrate && python manage.py collectstatic --noinput"
```

### 4. Перезапуск сервисов
```bash
systemctl start barlau
systemctl restart nginx
```

### 5. Проверка
```bash
# Проверить статус сервиса
systemctl status barlau

# Проверить логи
journalctl -u barlau -f

# Проверить новый API
curl https://barlau.org/api/public-notifications/
```

## Результат
После развертывания:
- Авторизованные пользователи будут получать свои уведомления через `/api/notifications/`
- Неавторизованные пользователи будут видеть последние 10 уведомлений через `/api/public-notifications/`
- Интерфейс автоматически переключится на публичный API при необходимости

## Тестирование
1. Откройте https://barlau.org
2. Нажмите на иконку уведомлений (колокольчик)
3. Должны отобразиться уведомления

## Создание тестового уведомления
```bash
# На сервере в Django shell
python manage.py shell
```

```python
# В Django shell
from accounts.models import User
from core.models import Notification

admin = User.objects.filter(role='SUPERADMIN').first()
if admin:
    Notification.create_system_notification(
        admin,
        "Тест уведомлений",
        "Система уведомлений работает корректно!"
    )
    print("✅ Тестовое уведомление создано")
``` 