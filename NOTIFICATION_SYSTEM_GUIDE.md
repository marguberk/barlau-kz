# 🔔 Система уведомлений BARLAU.KZ

## 📋 Обзор системы

Система уведомлений BARLAU.KZ реализована с использованием Django signals для автоматической отправки уведомлений при важных событиях в системе.

## 🎯 Основные возможности

### ✅ Автоматические уведомления для:
- **Задачи**: создание, изменение статуса, назначение исполнителей
- **Расходы**: добавление новых расходов с приоритизацией по сумме
- **Поездки**: создание, изменение статуса, начало/завершение
- **Транспорт**: добавление нового транспорта, требование техобслуживания
- **Документы**: истечение сроков документов транспорта
- **Системные**: важные системные события

### 👥 Получатели уведомлений по ролям:

**Руководящий состав** (получают большинство уведомлений):
- DIRECTOR (Директор)
- ADMIN (Администратор)
- SUPERADMIN (Суперадмин)
- DISPATCHER (Диспетчер)

**Финансовые сотрудники** (уведомления о расходах):
- DIRECTOR (Директор)
- ADMIN (Администратор)
- SUPERADMIN (Суперадмин)
- ACCOUNTANT (Бухгалтер)

## 🔧 Архитектура системы

### 1. Модель Notification

```python
class Notification(models.Model):
    # Типы уведомлений
    class Type(models.TextChoices):
        TASK = 'TASK', 'Задача'
        WAYBILL = 'WAYBILL', 'Путевой лист'
        EXPENSE = 'EXPENSE', 'Расход'
        SYSTEM = 'SYSTEM', 'Системное'
        DOCUMENT = 'DOCUMENT', 'Документ'
        TRIP = 'TRIP', 'Поездка'
        VEHICLE = 'VEHICLE', 'Транспорт'
        URGENT = 'URGENT', 'Срочное'
        INFO = 'INFO', 'Информация'
    
    # Приоритеты
    class Priority(models.TextChoices):
        LOW = 'LOW', 'Низкий'
        NORMAL = 'NORMAL', 'Обычный'
        HIGH = 'HIGH', 'Высокий'
        URGENT = 'URGENT', 'Срочный'
```

### 2. NotificationService

Централизованный сервис для отправки уведомлений множественным получателям:

```python
# Получение получателей по ролям
recipients = NotificationService.get_management_recipients()
financial_recipients = NotificationService.get_financial_recipients()

# Массовая отправка
NotificationService.send_to_multiple_users(
    recipients=recipients,
    notification_type=Notification.Type.TASK,
    title='Новая задача',
    message='Создана новая задача...',
    link='/dashboard/tasks/'
)
```

## 📊 События и уведомления

### 1. 📋 Задачи

**При создании задачи:**
- Исполнитель получает уведомление о назначении
- Руководство получает уведомление о создании новой задачи

**При изменении статуса:**
- Создатель задачи получает уведомление об изменении
- Руководство получает уведомление об изменении статуса

### 2. 💰 Расходы

**При добавлении расхода:**
- Финансовые сотрудники получают уведомление
- Приоритет зависит от суммы:
  - > 100,000 тг → HIGH
  - > 50,000 тг → NORMAL  
  - < 50,000 тг → LOW

### 3. 🚗 Поездки

**При создании поездки:**
- Водитель получает уведомление о назначении
- Руководство получает уведомление о новой поездке

**При изменении статуса:**
- Водитель получает уведомление об изменении
- Руководство получает уведомление об изменении статуса

### 4. 🚛 Транспорт

**При добавлении транспорта:**
- Руководство получает уведомление о новом транспорте

### 5. 📄 Документы транспорта

**При истечении сроков:**
- За 30, 14, 7, 3, 1 день и в день истечения
- Приоритет зависит от времени:
  - Истек/завтра → URGENT
  - До 3 дней → URGENT
  - До 7 дней → HIGH
  - До 30 дней → NORMAL

## ⏰ Автоматизация

### Проверка документов через cron

```bash
# Каждый день в 9:00 утра
0 9 * * * cd /path/to/project && source venv/bin/activate && python manage.py check_expiring_documents --verbose

# Каждые 6 часов для критических проверок
0 */6 * * * cd /path/to/project && source venv/bin/activate && python manage.py check_expiring_documents
```

### Команды управления

```bash
# Проверка истекающих документов
python manage.py check_expiring_documents --verbose

# Проверка истекающих документов за 7 дней
python manage.py check_expiring_documents --days 7
```

## 🛠 Настройка

### 1. Подключение signals

Signals автоматически подключаются через `core/apps.py`:

```python
class CoreConfig(AppConfig):
    def ready(self):
        import core.signals
```

### 2. Логирование

Добавьте в `settings.py`:

```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': 'notifications.log',
        },
    },
    'loggers': {
        'core.signals': {
            'handlers': ['file'],
            'level': 'INFO',
            'propagate': True,
        },
    },
}
```

## 🔧 API для уведомлений

### Получение уведомлений

```javascript
// Получить все уведомления
GET /api/notifications/

// Получить непрочитанные
GET /api/notifications/?unread=true

// Получить по типу
GET /api/notifications/?type=TASK

// Отметить все как прочитанные
POST /api/notifications/mark_all_read/
```

### Создание уведомлений программно

```python
from core.models import Notification

# Системное уведомление
Notification.create_system_notification(
    user=user,
    title='Важное сообщение',
    message='Описание события...',
    priority=Notification.Priority.HIGH
)

# Уведомление о документе
Notification.create_document_expiry_notification(
    user=user,
    vehicle=vehicle,
    document_type='Техпаспорт',
    expiry_date=expiry_date,
    days_left=7
)

# Массовые уведомления
recipients = User.objects.filter(role='DIRECTOR')
Notification.bulk_create_notifications(
    recipients=recipients,
    notification_type=Notification.Type.URGENT,
    title='Срочное уведомление',
    message='Требуется немедленное внимание'
)
```

## 📱 Фронтенд интеграция

### Отображение приоритетов

```javascript
const getPriorityClass = (priority) => {
    switch(priority) {
        case 'URGENT': return 'bg-red-500 text-white';
        case 'HIGH': return 'bg-orange-500 text-white';
        case 'NORMAL': return 'bg-blue-500 text-white';
        case 'LOW': return 'bg-gray-500 text-white';
        default: return 'bg-gray-300';
    }
};
```

### Звуковые уведомления

Система поддерживает воспроизведение звуков для срочных уведомлений:

```javascript
// В core/static/core/js/main.js
function showToastNotification(title, message, link, type) {
    // Воспроизводится звук для срочных уведомлений
    if (type === 'URGENT' || title.includes('СРОЧНО')) {
        playNotificationSound();
    }
}
```

## 🐛 Отладка

### Проверка работы signals

```python
# В Django shell
python manage.py shell

from logistics.models import Task, Expense
from core.models import Notification

# Создать тестовую задачу
task = Task.objects.create(
    title="Тестовая задача",
    description="Описание",
    assigned_to_id=1,
    created_by_id=1,
    due_date="2025-01-20"
)

# Проверить созданные уведомления
notifications = Notification.objects.filter(type='TASK').order_by('-created_at')[:5]
for n in notifications:
    print(f"{n.user.email}: {n.title}")
```

### Проверка истечения документов

```bash
# Запустить проверку вручную
python manage.py check_expiring_documents --verbose

# Проверить логи
tail -f notifications.log
```

## ⚡ Производительность

### Оптимизация запросов

- Используется `bulk_create` для массовых уведомлений
- Добавлены индексы для часто используемых полей
- Проверка дубликатов документов предотвращает спам

### Очистка старых уведомлений

```python
# Удалить прочитанные уведомления старше 30 дней
from datetime import timedelta
from django.utils import timezone

old_date = timezone.now() - timedelta(days=30)
Notification.objects.filter(
    read=True,
    created_at__lt=old_date
).delete()
```

## 🚀 Будущие улучшения

- [ ] Email уведомления для критических событий
- [ ] Push уведомления для мобильных приложений
- [ ] Настройки уведомлений для каждого пользователя
- [ ] Группировка похожих уведомлений
- [ ] Статистика по уведомлениям

## 🔐 Безопасность

- Все уведомления привязаны к конкретным пользователям
- Доступ к уведомлениям через API требует аутентификации
- Уведомления отправляются только активным пользователям
- Логирование всех операций с уведомлениями 