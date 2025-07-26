# Исправление Django API endpoint для обновления профиля

## Проблема
При попытке обновить профиль пользователя в Flutter приложении возникала ошибка HTTP 405 (Method Not Allowed). Endpoint `/api/v1/users/me/` поддерживал только GET метод, но не поддерживал PUT/PATCH методы для обновления данных.

## Причина
В `UserViewSet` в `accounts/views.py` endpoint `me` был настроен только для GET запросов:

```python
@action(detail=False, methods=['get'])
def me(self, request):
    serializer = UserSerializer(request.user)
    return Response(serializer.data)
```

## Решение

### Обновлен endpoint `me` в `UserViewSet`

```python
@action(detail=False, methods=['get', 'put', 'patch'])
def me(self, request):
    if request.method == 'GET':
        serializer = UserSerializer(request.user)
        return Response(serializer.data)
    elif request.method in ['PUT', 'PATCH']:
        serializer = UserUpdateSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

### Что изменилось:

1. **Добавлены методы PUT и PATCH** в `methods=['get', 'put', 'patch']`
2. **Добавлена логика обработки PUT/PATCH запросов** для обновления профиля
3. **Используется `UserUpdateSerializer`** для валидации и сохранения данных
4. **Поддержка частичного обновления** через `partial=True`

## API Endpoints

### GET /api/v1/users/me/
- **Назначение**: Получение данных текущего пользователя
- **Метод**: GET
- **Headers**: `Authorization: Bearer <token>`
- **Ответ**: JSON с данными пользователя

### PUT /api/v1/users/me/
- **Назначение**: Обновление профиля текущего пользователя
- **Метод**: PUT
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Body**: JSON с полями для обновления
- **Ответ**: JSON с обновленными данными пользователя

### PATCH /api/v1/users/me/
- **Назначение**: Частичное обновление профиля текущего пользователя
- **Метод**: PATCH
- **Headers**: `Authorization: Bearer <token>`, `Content-Type: application/json`
- **Body**: JSON с полями для обновления
- **Ответ**: JSON с обновленными данными пользователя

## Поддерживаемые поля для обновления

Согласно `UserUpdateSerializer`, можно обновлять следующие поля:
- `email`
- `phone`
- `first_name`
- `last_name`
- `position`
- `experience`
- `education`
- `skills`
- `photo`

## Тестирование

### 1. Получение токена
```bash
curl -X POST http://localhost:8000/api/v1/auth/token/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

### 2. Получение данных пользователя
```bash
curl -X GET http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer <token>"
```

### 3. Обновление профиля
```bash
curl -X PUT http://localhost:8000/api/v1/users/me/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{"first_name":"Админ","last_name":"Истратор","email":"admin@barlau.org","phone":"+77777777777"}'
```

## Результат

✅ **HTTP 405 ошибка исправлена** - endpoint теперь поддерживает PUT/PATCH методы
✅ **Обновление профиля работает** - данные сохраняются в базе данных
✅ **Валидация данных** - проверка уникальности email и телефона
✅ **Частичное обновление** - можно обновлять только нужные поля
✅ **Безопасность** - только авторизованные пользователи могут обновлять свой профиль

## Интеграция с Flutter

Теперь Flutter приложение может успешно обновлять профиль пользователя через API endpoint `/api/v1/users/me/` с помощью PUT запроса. Изменения сохраняются в базе данных и остаются после перезапуска приложения. 