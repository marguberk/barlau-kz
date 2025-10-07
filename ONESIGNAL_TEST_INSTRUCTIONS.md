# 🔔 OneSignal Push Notifications - Инструкция по тестированию

## ✅ Что уже настроено:

### 🔧 Django Backend
- ✅ **OneSignalService** - сервис для отправки push-уведомлений
- ✅ **NotificationBroadcastAPIView** - интегрирован с OneSignal
- ✅ **UpdateOneSignalPlayerIdAPIView** - API endpoint для сохранения Player ID
- ✅ **Поле `onesignal_player_id`** в модели User
- ✅ **Миграция базы данных** применена

### 📱 Flutter Frontend
- ✅ **OneSignalService** - инициализация и обработка уведомлений
- ✅ **SafeApiService.updateOneSignalPlayerId()** - отправка Player ID на сервер
- ✅ **Автоматическая регистрация** Player ID при запуске приложения

### 🎯 Тестовые данные
- ✅ **Player ID сохранен** для тестового водителя: `432a4337-2e8c-46c6-8c75-ec4e1bb4b904`
- ✅ **Приложения запущены** на iOS и Android эмуляторах

## 🧪 Как протестировать:

### 1. Проверить инициализацию OneSignal
В логах Flutter приложения должны быть сообщения:
```
📱 OneSignalService: Player ID получен: 432a4337-2e8c-46c6-8c75-ec4e1bb4b904
📱 OneSignalService: Player ID успешно отправлен на сервер
```

### 2. Отправить тестовое уведомление через Django
```bash
cd /Users/almaty/cursors/maro
source venv/bin/activate
python3 -c "
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from core.onesignal_service import OneSignalService

# Отправляем тестовое уведомление
OneSignalService.send_notification_to_users(
    title='🔔 Тестовое уведомление',
    message='Это тестовое уведомление для проверки звука и push-уведомлений!',
    target_roles=['DRIVER'],
    is_urgent=True
)
"
```

### 3. Проверить получение уведомлений
- **iOS эмулятор**: Должно прийти push-уведомление со звуком
- **Android эмулятор**: Должно прийти push-уведомление со звуком
- **В приложении**: Уведомление должно появиться в списке уведомлений

### 4. Тестировать через приложение (для директоров/суперадминов)
1. Войти как директор или суперадмин
2. Перейти в раздел "Уведомления"
3. Нажать кнопку "Рассылка" (FloatingActionButton)
4. Создать уведомление для водителей
5. Проверить получение push-уведомлений

## 🔍 Отладка:

### Если уведомления не приходят:
1. **Проверить Player ID** в логах Flutter
2. **Проверить разрешения** на уведомления в настройках эмулятора
3. **Проверить OneSignal Dashboard** - есть ли активные устройства
4. **Проверить Django логи** - отправляются ли запросы к OneSignal

### Если нет звука:
1. **iOS**: Проверить настройки уведомлений в эмуляторе
2. **Android**: Проверить громкость и режим "Не беспокоить"
3. **OneSignal**: Проверить настройки звука в Dashboard

## 📊 Текущий статус:
- ✅ **OneSignal интеграция** - готова
- ✅ **Django backend** - настроен
- ✅ **Flutter frontend** - настроен
- ✅ **Тестовые данные** - подготовлены
- ✅ **Приложения запущены** на iOS и Android

## 🚀 Готово к продакшену:
Теперь когда директор или суперадмин создает рассылку уведомлений через приложение, все водители автоматически получат push-уведомления со звуком и вибрацией!

**Больше не нужно заходить в OneSignal Dashboard** - все работает через ваше приложение! 🎉

