# Исправление проблемы с сохранением профиля

## Проблема
При редактировании профиля (имя, фамилия, фото и т.д.) изменения сохранялись только в текущем сеансе. После выхода из аккаунта и повторного входа все изменения терялись.

## Причина
Метод `updateProfile` в `AuthProvider` обновлял только локальные данные, но не отправлял изменения на сервер Django.

## Решение

### 1. Добавлен метод `updateUserProfile` в `SafeApiService`

```dart
static Future<Map<String, dynamic>> updateUserProfile({
  required String firstName,
  required String lastName,
  required String email,
  required String phone,
  String? profilePicture,
  bool removeAvatar = false,
}) async {
  // Получаем токен авторизации
  final prefs = await SharedPreferences.getInstance();
  final token = prefs.getString('auth_token');
  
  // Подготавливаем данные для отправки
  final updateData = <String, dynamic>{
    'first_name': firstName,
    'last_name': lastName,
    'email': email,
    'phone': phone,
  };

  if (removeAvatar) {
    updateData['profile_picture'] = null;
  } else if (profilePicture != null) {
    updateData['profile_picture'] = profilePicture;
  }

  // Отправляем запрос на обновление профиля
  final result = await safeRequest('/v1/users/me/', 
    method: 'PUT',
    headers: {
      'Authorization': 'Bearer $token',
    },
    body: updateData,
  );

  if (result['success'] && result['data'] != null) {
    // Обновляем локальные данные пользователя
    await prefs.setString('user_profile', jsonEncode(result['data']));
    
    return {
      'success': true,
      'data': result['data'],
    };
  } else {
    return {
      'success': false,
      'error': result['error'] ?? 'Ошибка обновления профиля',
    };
  }
}
```

### 2. Обновлен метод `updateProfile` в `AuthProvider`

```dart
Future<bool> updateProfile({
  required String firstName,
  required String lastName,
  required String email,
  required String phone,
  String? profilePicture,
  bool removeAvatar = false,
}) async {
  // Отправляем обновление на сервер через SafeApiService
  final result = await SafeApiService.updateUserProfile(
    firstName: firstName,
    lastName: lastName,
    email: email,
    phone: phone,
    profilePicture: profilePicture,
    removeAvatar: removeAvatar,
  );

  if (result['success'] && result['data'] != null) {
    // Обновляем локальный объект пользователя
    final userData = result['data'];
    _user = User(
      id: _user!.id,
      username: _user!.username,
      firstName: userData['first_name'] ?? firstName,
      lastName: userData['last_name'] ?? lastName,
      email: userData['email'] ?? email,
      phone: userData['phone'] ?? phone,
      role: _user!.role,
      isActive: _user!.isActive,
      profilePicture: userData['profile_picture'] ?? _user!.profilePicture,
    );

    // Сохраняем обновленный профиль локально
    await _saveUserToLocal(_user!);
    
    return true;
  } else {
    _error = result['error'] ?? 'Ошибка обновления профиля';
    return false;
  }
}
```

## Результат

Теперь при редактировании профиля:

1. **Изменения отправляются на сервер Django** через API endpoint `/v1/users/me/`
2. **Локальные данные обновляются** только после успешного сохранения на сервере
3. **Изменения сохраняются между сеансами** - после выхода и повторного входа профиль остается обновленным
4. **Обработка ошибок** - если сервер недоступен или произошла ошибка, пользователь получает уведомление

## API Endpoint

Используется Django REST Framework endpoint:
- **URL**: `PUT /api/v1/users/me/`
- **Headers**: `Authorization: Bearer <token>`
- **Body**: JSON с полями `first_name`, `last_name`, `email`, `phone`, `profile_picture`

## Тестирование

Для тестирования:
1. Запустить Django сервер: `python manage.py runserver`
2. Запустить Flutter приложение
3. Войти в аккаунт
4. Отредактировать профиль
5. Выйти из аккаунта
6. Войти снова - изменения должны сохраниться 