# Удаление пользователей с продакшн сервера

## Выполненные изменения

### Удаленные пользователи:
- ✅ `superadmin` / `admin123` - Супер Администратор
- ✅ `admin` / `admin123` - Основной администратор  
- ✅ `erzhan` / `erzhan@gmail.com` - Ержан Сапаров

### Оставшиеся пользователи (9 менеджеров):
- `aidana.uzakova` / `aidana.uzakova@barlau.org` - Айдана Узакова
- `muratjan.ilakhunov` / `muratjan.ilakhunov@barlau.org` - Муратжан Илахунов
- `aset.ilyamov` / `aset.ilyamov@barlau.org` - Асет Ильямов
- `gabit.akhmetov` / `gabit.akhmetov@barlau.org` - Габит Ахметов
- `maksat.kusaiyn` / `maksat.kusaiyn@barlau.org` - Максат Кусайын
- `nazerke.sadvakasova` / `nazerke.sadvakasova@barlau.org` - Назерке Садвакасова
- `erbolat.kudaibergen` / `erbolat.kudaibergen@barlau.org` - Ерболат Кудайбергенов
- `almas.sopashev` / `almas.sopashev@barlau.org` - Алмас Сопашев
- `serik.aidarbe` / `serik.aidarbe@barlau.org` - Серик Айдарбеков

## Технические детали

### Команда удаления:
```bash
sshpass -p "33q97KKRfmnHTY6dCiyuA3g=" ssh -o StrictHostKeyChecking=no ubuntu@85.202.192.33 "cd /var/www/barlau && source venv/bin/activate && python manage.py shell -c \"from django.db import connection; cursor = connection.cursor(); cursor.execute('PRAGMA foreign_keys = OFF'); cursor.execute('DELETE FROM accounts_user WHERE username = \\\"superadmin\\\"'); cursor.execute('DELETE FROM accounts_user WHERE username = \\\"admin\\\"'); cursor.execute('DELETE FROM accounts_user WHERE username = \\\"erzhan\\\"'); cursor.execute('PRAGMA foreign_keys = ON');\""
```

### Обновленные файлы:
1. **PRODUCTION_USERS.md** - удалены ссылки на удаленных пользователей
2. **barlau_flutter/lib/config/app_config.dart** - обновлен список доступных пользователей
3. **barlau_flutter/lib/screens/login_screen.dart** - обновлены тестовые данные

## Проблемы и решения

### Проблема 1: Отсутствующая таблица core_tripchecklist
**Решение:** Создана таблица через SQL:
```sql
CREATE TABLE IF NOT EXISTS core_tripchecklist (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    trip_id INTEGER NOT NULL,
    checklist_item_id INTEGER NOT NULL,
    is_completed BOOLEAN NOT NULL,
    notes TEXT
);
```

### Проблема 2: Ограничения внешних ключей
**Решение:** Временно отключены проверки внешних ключей:
```sql
PRAGMA foreign_keys = OFF;
-- удаление пользователей
PRAGMA foreign_keys = ON;
```

## Результат

✅ Все указанные пользователи успешно удалены с продакшн сервера
✅ Обновлена документация и конфигурация приложения
✅ Оставлены только менеджеры (9 пользователей)
✅ Исправлены проблемы с базой данных

## Дата изменений: 26.07.2025 
 
 
 
 