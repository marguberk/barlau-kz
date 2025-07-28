# Изменение иконок меню в Flutter приложении

## Выполненные изменения

### 1. Удаление пользователей с продакшн сервера

**Удалены следующие пользователи:**
- `testuser` / `testuser@barlau.org`
- `test123` / `test123@test.com`
- `user1` / `user1@barlau.org` - Асылбек
- `user2` / `user2@barlau.org` - Жанар
- `user3` / `user3@barlau.org` - Марат
- `user4` / `user4@barlau.org` - Айгуль

**Оставшиеся пользователи:**
- `admin` / `admin123` - Основной администратор
- `superadmin` / `admin123` - Супер администратор
- `erzhan` / `erzhan@gmail.com` - Ержан Сапаров
- `aidana.uzakova` / `aidana.uzakova@barlau.org` - Айдана Узакова
- `muratjan.ilakhunov` / `muratjan.ilakhunov@barlau.org` - Муратжан Илахунов
- `aset.ilyamov` / `aset.ilyamov@barlau.org` - Асет Ильямов
- `gabit.akhmetov` / `gabit.akhmetov@barlau.org` - Габит Ахметов
- `maksat.kusaiyn` / `maksat.kusaiyn@barlau.org` - Максат Кусайын
- `nazerke.sadvakasova` / `nazerke.sadvakasova@barlau.org` - Назерке Садвакасова
- `erbolat.kudaibergen` / `erbolat.kudaibergen@barlau.org` - Ерболат Кудайбергенов
- `almas.sopashev` / `almas.sopashev@barlau.org` - Алмас Сопашев
- `serik.aidarbe` / `serik.aidarbe@barlau.org` - Серик Айдарбеков

### 2. Изменение иконок меню

**Файл:** `barlau_flutter/lib/screens/main_screen.dart`

**До изменений:**
- **Заезды:** `truck.svg` (иконка грузовика)
- **Грузовики:** `location.svg` (иконка локации)

**После изменений:**
- **Заезды:** `location.svg` (иконка локации)
- **Грузовики:** `truck.svg` (иконка грузовика)

### 3. Обновление конфигурации

**Файл:** `barlau_flutter/lib/config/app_config.dart`

Удалены ссылки на удаленных пользователей из `availableUsers`.

## Технические детали

### Команда удаления пользователей:
```bash
sshpass -p "33q97KKRfmnHTY6dCiyuA3g=" ssh -o StrictHostKeyChecking=no ubuntu@85.202.192.33 "cd /var/www/barlau && source venv/bin/activate && python manage.py shell -c \"from django.contrib.auth import get_user_model; User = get_user_model(); User.objects.filter(username__in=['testuser', 'test123', 'user1', 'user2', 'user3', 'user4']).delete()\""
```

### Изменения в коде:
```dart
// Было:
label: 'Заезды', assetName: 'truck.svg'
label: 'Грузовики', assetName: 'location.svg'

// Стало:
label: 'Заезды', assetName: 'location.svg'
label: 'Грузовики', assetName: 'truck.svg'
```

## Результат

1. ✅ Удалены все testuser и водители (кроме Армана и Юнуса)
2. ✅ Поменяны местами иконки пунктов меню "Грузовики" и "Заезды"
3. ✅ Обновлена документация и конфигурация

## Дата изменений: 26.07.2025 
 
 
 
 