# BARLAU.KZ - Мобильное приложение

Мобильное приложение для системы управления логистикой BARLAU.KZ, созданное с использованием React Native и Expo.

## 🚀 Функциональность

- **Аутентификация**: Вход в систему через логин и пароль
- **Дашборд**: Главная страница со статистикой и последними обновлениями
- **Карта**: Отслеживание местоположения водителей в реальном времени
- **Задачи**: Управление задачами и их статусами
- **Уведомления**: Push-уведомления о важных событиях
- **Профиль**: Управление профилем пользователя

## 📋 Требования

- Node.js 18+
- npm или yarn
- Expo CLI (`npm install -g expo-cli`)
- iOS Simulator (для iOS) или Android Studio (для Android)

## 🛠️ Установка и запуск

### 1. Клонирование и установка зависимостей

```bash
cd barlau-mobile
npm install
```

### 2. Настройка API

Отредактируйте файл `src/services/api.ts` и замените BASE_URL на ваш сервер:

```typescript
const BASE_URL = 'https://your-domain.com/api'; // Ваш Django API
```

### 3. Запуск приложения

```bash
npm start
# или
expo start
```

## 📱 Сборка приложения

### Для iOS

```bash
# Сборка для iOS (требуется macOS)
expo build:ios

# Или с EAS Build
npx eas build --platform ios
```

### Для Android

```bash
# Сборка для Android
expo build:android

# Или с EAS Build
npx eas build --platform android
```

## 🔧 Настройка Django API

Для корректной работы мобильного приложения необходимо настроить ваш Django сервер:

### 1. Добавление CORS Headers

Установите django-cors-headers:

```bash
pip install django-cors-headers
```

В `settings.py`:

```python
INSTALLED_APPS = [
    # ...
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    # ...
]

# Для разработки
CORS_ALLOW_ALL_ORIGINS = True

# Для продакшена укажите конкретные домены
# CORS_ALLOWED_ORIGINS = [
#     "http://localhost:19006",  # Expo dev server
# ]
```

### 2. Настройка аутентификации

Убедитесь, что у вас настроен JWT в Django:

```python
# settings.py
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}

from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
}
```

### 3. Необходимые API endpoints

Убедитесь, что в Django есть следующие endpoints:

```python
# urls.py
urlpatterns = [
    path('api/auth/login/', obtain_jwt_token, name='token_obtain_pair'),
    path('api/auth/refresh/', refresh_jwt_token, name='token_refresh'),
    path('api/auth/user/', current_user_view, name='current_user'),
    path('api/logistics/tasks/', TaskViewSet.as_view({'get': 'list'})),
    path('api/logistics/vehicles/', VehicleViewSet.as_view({'get': 'list'})),
    path('api/core/notifications/', NotificationViewSet.as_view({'get': 'list'})),
    path('api/core/driver_locations/', driver_locations_api),
    path('api/map/tracking_status/', update_tracking_status),
]
```

## 📦 Структура проекта

```
barlau-mobile/
├── src/
│   ├── components/          # Переиспользуемые компоненты
│   │   ├── LoginScreen.tsx
│   │   ├── DashboardScreen.tsx
│   │   └── MapScreen.tsx
│   ├── context/            # React Context (AuthContext)
│   ├── screens/            # Экраны приложения
│   └── services/           # API сервисы
├── assets/                 # Изображения, иконки
├── App.tsx                 # Главный компонент
├── app.json               # Конфигурация Expo
└── package.json
```

## 🎨 Дизайн и UI

Приложение использует современный дизайн с:
- Цветовая схема: синий (#2563EB) как основной цвет
- Адаптивный дизайн для разных размеров экранов
- Тени и скругленные углы для современного вида
- Интуитивная навигация с bottom tabs

## 🔒 Безопасность

- JWT токены для аутентификации
- Автоматическое обновление токенов
- Безопасное хранение данных с AsyncStorage
- Валидация на стороне клиента и сервера

## 📊 Отслеживание местоположения

Для водителей доступна функция отслеживания местоположения:
- Запрос разрешений на геолокацию
- Отправка координат каждые 30 секунд
- Отображение на карте для диспетчеров и админов

## 🔔 Push-уведомления

Настройка push-уведомлений через Expo:

```typescript
import * as Notifications from 'expo-notifications';

// Регистрация для получения push-токена
const token = await Notifications.getExpoPushTokenAsync();
```

## 🚀 Публикация в App Store и Google Play

### App Store (iOS)

1. Создайте Apple Developer аккаунт ($99/год)
2. Соберите приложение: `expo build:ios`
3. Загрузите через App Store Connect
4. Пройдите процесс ревью Apple

### Google Play (Android)

1. Создайте Google Play Developer аккаунт ($25 однократно)
2. Соберите приложение: `expo build:android`
3. Загрузите APK/AAB в Google Play Console
4. Заполните описание приложения

## 📈 Мониторинг и аналитика

Интеграция с сервисами аналитики:

```bash
npm install @react-native-async-storage/async-storage
npm install @react-native-community/netinfo
```

## 🔧 Troubleshooting

### Частые проблемы:

1. **Ошибка сети**: Проверьте BASE_URL в api.ts
2. **Проблемы с картой**: Убедитесь, что разрешения на геолокацию выданы
3. **JWT токены**: Проверьте настройки CORS на сервере

### Логи и отладка:

```bash
# Посмотреть логи
npx react-native log-ios
npx react-native log-android

# Очистить кэш
expo r -c
```

## 🤝 Поддержка

Для получения поддержки:
- Создайте issue в репозитории
- Обратитесь к документации Expo: https://docs.expo.dev/
- React Navigation: https://reactnavigation.org/

## 📄 Лицензия

Proprietary - BARLAU.KZ

---

**Версия**: 1.0.0  
**Последнее обновление**: $(date)  
**Разработчик**: BARLAU.KZ Team 