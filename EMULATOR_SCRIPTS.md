# 📱 Скрипты управления Flutter эмуляторами

Набор скриптов для удобного управления iOS и Android эмуляторами Flutter приложения BARLAU.KZ.

## 🚀 Доступные скрипты

### 1. `restart_emulators.sh` - Полный перезапуск эмуляторов
Подробный скрипт с диагностикой и автоматическим запуском эмуляторов.

```bash
./restart_emulators.sh
```

**Что делает:**
- ✅ Останавливает все Flutter процессы
- ✅ Проверяет доступные устройства
- ✅ Автоматически запускает iOS симулятор (iPhone 16 Pro)
- ✅ Автоматически запускает Android эмулятор (Pixel_7)
- ✅ Запускает Flutter приложения на обоих устройствах
- ✅ Показывает статус процессов и полезные команды

### 2. `restart.sh` - Быстрый перезапуск
Минималистичный скрипт для быстрого перезапуска приложений.

```bash
./restart.sh
```

**Что делает:**
- ⚡ Быстро убивает Flutter процессы
- ⚡ Запускает приложения в фоновом режиме
- ⚡ Показывает статус процессов

### 3. `stop_emulators.sh` - Остановка всех эмуляторов
Полная остановка всех Flutter приложений и эмуляторов.

```bash
./stop_emulators.sh
```

**Что делает:**
- 🛑 Останавливает все Flutter процессы
- 🛑 Закрывает Android эмуляторы
- 🛑 Закрывает iOS симуляторы
- 🛑 Показывает статус очистки

## 🎯 ID устройств

### Android эмулятор
- **ID:** `emulator-5554`
- **Устройство:** Pixel 7 (Android 14 API 34)

### iOS симулятор  
- **ID:** `294C60FA-C0C4-48A2-A075-BA293F671E39`
- **Устройство:** iPhone 16 Pro (iOS 18.4)

## 🔧 Полезные команды

### Просмотр логов
```bash
# Android логи
flutter logs -d emulator-5554

# iOS логи  
flutter logs -d 294C60FA-C0C4-48A2-A075-BA293F671E39
```

### Hot reload/restart
В активном терминале Flutter:
- **Hot reload:** нажмите `r`
- **Hot restart:** нажмите `R`
- **Очистка консоли:** нажмите `c`
- **Выход:** нажмите `q`

### Проверка статуса
```bash
# Список всех устройств
flutter devices

# Активные Flutter процессы
ps aux | grep "flutter.*run" | grep -v grep

# Проверка продакшн API
curl -s https://barlau.org/api/vehicles/ | head -5
```

### Управление эмуляторами вручную
```bash
# Запуск Android эмулятора
flutter emulators --launch Pixel_7

# Запуск iOS симулятора
open -a Simulator
xcrun simctl boot "iPhone 16 Pro"

# Остановка iOS симулятора
xcrun simctl shutdown all
```

## 📊 Конфигурация приложения

### API подключения
- **iOS/Android устройства:** `https://barlau.org/api` (продакшн)
- **Веб/Desktop:** `http://localhost:8000/api` (в debug режиме)
- **Веб (продакшн):** `https://barlau.org/api`

### Фильтрация сотрудников
Обычные пользователи видят только роли:
- `DIRECTOR`, `DRIVER`, `MANAGER`, `ACCOUNTANT`
- `CONSULTANT`, `TECH`, `SUPPLIER`, `DISPATCHER`
- `LOGIST`, `IT_MANAGER`, `EMPLOYEE`

Скрыты роли: `SUPERADMIN`, `ADMIN`

## 🚨 Устранение неполадок

### Эмулятор не запускается
```bash
# Проверка доступных эмуляторов
flutter emulators

# Сброс Flutter
flutter clean && flutter pub get

# Перезапуск Android Studio/Xcode
```

### Ошибки сборки
```bash
# Очистка кэша
cd barlau_flutter
flutter clean
flutter pub get

# Пересборка
flutter run -d emulator-5554 --no-cached-dependencies
```

### Проблемы с API
```bash
# Проверка локального сервера
curl http://localhost:8000/api/employees/

# Проверка продакшн сервера  
curl https://barlau.org/api/vehicles/
```

## 📁 Структура проекта

```
maro/
├── restart_emulators.sh    # Полный перезапуск
├── restart.sh              # Быстрый перезапуск  
├── stop_emulators.sh       # Остановка всех
├── EMULATOR_SCRIPTS.md     # Эта документация
└── barlau_flutter/         # Flutter проект
    ├── lib/
    │   ├── config/app_config.dart    # Конфигурация API
    │   ├── screens/employees_screen.dart  # Фильтрация сотрудников
    │   └── ...
    └── ...
```

---
**💡 Совет:** Используйте `restart.sh` для быстрых итераций разработки и `restart_emulators.sh` при первом запуске или проблемах с эмуляторами. 