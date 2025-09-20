import 'package:flutter/foundation.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import 'dart:convert';
import '../models/user.dart';
import '../services/api_service.dart';
import '../services/safe_api_service.dart';
import '../services/biometric_service.dart';

class AuthProvider with ChangeNotifier {
  User? _user;
  bool _isLoading = false;
  bool _isAuthenticated = false;
  String? _error;

  final ApiService _apiService = ApiService();

  User? get user => _user;
  bool get isLoading => _isLoading;
  bool get isAuthenticated => _isAuthenticated;
  String? get error => _error;

  // Сохранение пользователя в локальное хранилище
  Future<void> _saveUserToLocal(User user) async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final userJson = json.encode(user.toJson());
      await prefs.setString('user_profile', userJson);
      print('AuthProvider: Профиль сохранен локально');
    } catch (e) {
      print('AuthProvider: Ошибка сохранения профиля: $e');
    }
  }

  // Загрузка пользователя из локального хранилища
  Future<User?> _loadUserFromLocal() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      final userJson = prefs.getString('user_profile');
      if (userJson != null) {
        final userMap = json.decode(userJson);
        print('AuthProvider: Профиль загружен из локального хранилища');
        return User.fromJson(userMap);
      }
    } catch (e) {
      print('AuthProvider: Ошибка загрузки профиля: $e');
    }
    return null;
  }



  // Получение данных пользователя для быстрого входа
  Map<String, String>? getUserDataForQuickLogin() {
    print('AuthProvider: getUserDataForQuickLogin - _user: ${_user != null ? "есть" : "null"}');
    if (_user != null) {
      final userData = {
        'username': _user!.username,
        'displayName': _user!.firstName.isNotEmpty ? '${_user!.firstName} ${_user!.lastName}'.trim() : _user!.username,
        'firstName': _user!.firstName,
        'lastName': _user!.lastName,
      };
      print('AuthProvider: getUserDataForQuickLogin - данные: $userData');
      return userData;
    }
    print('AuthProvider: getUserDataForQuickLogin - пользователь не найден');
    return null;
  }

  // Удаление пользователя из локального хранилища
  Future<void> _removeUserFromLocal() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      // Удаляем все данные авторизации
      await prefs.remove('user_profile');
      await prefs.remove('auth_token');
      await prefs.remove('refresh_token');
      await prefs.remove('user_role');
      await prefs.remove('user_name');
      await prefs.remove('user_id');
      print('AuthProvider: Все данные авторизации удалены из локального хранилища');
    } catch (e) {
      print('AuthProvider: Ошибка удаления данных авторизации: $e');
    }
  }

  // Выход из-за недействительной сессии
  Future<void> _logoutDueToInvalidSession(String reason) async {
    print('AuthProvider: Выход из-за недействительной сессии: $reason');
    
    // Очищаем локальные данные
    await _removeUserFromLocal();
    
    // Очищаем состояние
    _user = null;
    _isAuthenticated = false;
    _error = reason;
    _isLoading = false;
    
    print('AuthProvider: Выход из-за недействительной сессии завершен');
  }

  // Публичный метод для выхода из-за истечения сессии
  Future<void> logoutDueToExpiredSession(String reason) async {
    await _logoutDueToInvalidSession(reason);
    notifyListeners();
  }

  Future<void> checkAuthStatus() async {
    _isLoading = true;
    notifyListeners();

    try {
      print('AuthProvider: Начинаем проверку статуса авторизации');
      
      // Проверяем все необходимые данные авторизации
      final prefs = await SharedPreferences.getInstance();
      final userProfile = prefs.getString('user_profile');
      final authToken = prefs.getString('auth_token');
      final userRole = prefs.getString('user_role');
      
      print('AuthProvider: Проверяем данные авторизации:');
      print('AuthProvider: user_profile: ${userProfile != null ? 'есть' : 'нет'}');
      print('AuthProvider: auth_token: ${authToken != null ? 'есть' : 'нет'}');
      print('AuthProvider: user_role: ${userRole != null ? 'есть' : 'нет'}');
      
      // Проверяем, есть ли все необходимые данные
      if (userProfile != null && authToken != null && userRole != null) {
        // Проверяем валидность токена
        print('AuthProvider: Проверяем валидность токена...');
        final validToken = await SafeApiService.getValidToken();
        
        if (validToken != null) {
          // Токен валиден, загружаем пользователя
          final localUser = await _loadUserFromLocal();
          if (localUser != null) {
            _user = localUser;
            _isAuthenticated = true;
            _error = null;
            print('AuthProvider: Пользователь авторизован - ${localUser.username} (${localUser.role})');
          } else {
            print('AuthProvider: Ошибка загрузки профиля пользователя');
            await _logoutDueToInvalidSession('Ошибка загрузки профиля');
          }
        } else {
          print('AuthProvider: Токен недействителен, выполняем выход');
          await _logoutDueToInvalidSession('Сессия истекла');
        }
      } else {
        print('AuthProvider: Неполные данные авторизации, требуется повторный вход');
        _isAuthenticated = false;
        _user = null;
        _error = null;
        // Очищаем неполные данные
        await _removeUserFromLocal();
      }
    } catch (e) {
      print('AuthProvider: Ошибка проверки авторизации: $e');
      await _logoutDueToInvalidSession('Ошибка проверки авторизации');
    }

    _isLoading = false;
    notifyListeners();
    print('AuthProvider: Статус авторизации: ${_isAuthenticated ? 'авторизован' : 'не авторизован'}');
  }

  Future<bool> login(String username, String password, {bool setupQuickLogin = false, BuildContext? context}) async {
    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
      print('AuthProvider: Попытка входа для пользователя $username');
      
      // Используем безопасный API
      final result = await SafeApiService.safeLogin(username, password);
      
      print('AuthProvider: Результат SafeApiService.safeLogin: ${result['success']}');
      print('AuthProvider: Данные пользователя: ${result['data']?['user']}');
      print('AuthProvider: result[data][user] != null: ${result['data']['user'] != null}');
      
      if (result['success']) {
        if (result['data']['user'] != null) {
          print('AuthProvider: Создаем пользователя из JSON');
          _user = User.fromJson(result['data']['user']);
          print('AuthProvider: Пользователь создан: ${_user!.username}, роль: ${_user!.role}');
          print('AuthProvider: Имя пользователя: ${_user!.firstName} ${_user!.lastName}');
          
          // Сохраняем пользователя локально
          await _saveUserToLocal(_user!);
          print('AuthProvider: Пользователь сохранен локально');
          
          // Дополнительно сохраняем ID пользователя
          final prefs = await SharedPreferences.getInstance();
          await prefs.setInt('user_id', _user!.id);
          print('AuthProvider: ID пользователя сохранен: ${_user!.id}');
        }
        _isAuthenticated = true;
        _error = null;
        print('AuthProvider: Авторизация успешна, устанавливаем _isAuthenticated = true');
        _isLoading = false;
        print('AuthProvider: Вызываем notifyListeners() после успешной авторизации');
        notifyListeners();
        print('AuthProvider: notifyListeners() вызван после успешной авторизации');
        
        // Навигация теперь управляется только LoginScreen
        // AuthProvider больше НЕ делает навигацию к PIN экрану
        
        // Дополнительно вызываем notifyListeners еще раз через небольшую задержку
        Future.delayed(const Duration(milliseconds: 100), () {
          print('AuthProvider: Дополнительный вызов notifyListeners()');
          notifyListeners();
        });
        
        return true;
      } else {
        print('AuthProvider: Авторизация неуспешна: ${result['error']}');
        _error = result['error'] ?? 'Неверный логин или пароль';
        _isAuthenticated = false;
        _user = null;
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      print('AuthProvider: Ошибка при входе - $e');
      _error = 'Ошибка входа в систему';
      _isAuthenticated = false;
      _user = null;
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }

  Future<void> logout() async {
    print('AuthProvider: Начинаем выход из аккаунта');
    _isLoading = true;
    notifyListeners();

    try {
      await _apiService.logout();
    } catch (e) {
      print('AuthProvider: Ошибка при вызове API logout: $e');
      // Игнорируем ошибки при выходе
    }

    // Сначала удаляем локальные данные
    await _removeUserFromLocal();
    
    // Затем очищаем состояние
    _user = null;
    _isAuthenticated = false;
    _error = null;
    _isLoading = false;
    
    // Очищаем данные быстрого входа при выходе
    try {
      await BiometricService.clearQuickLoginData();
      print('AuthProvider: Данные быстрого входа очищены при выходе');
    } catch (e) {
      print('AuthProvider: Ошибка очистки данных быстрого входа: $e');
    }
    
    print('AuthProvider: Выход из аккаунта завершен');
    notifyListeners();
    
    // Принудительно обновляем состояние для перехода на страницу входа
    await Future.delayed(const Duration(milliseconds: 100));
    notifyListeners();
  }

  void clearError() {
    _error = null;
    notifyListeners();
  }

  // Проверка валидности токена и автоматический выход при истечении
  Future<Map<String, dynamic>> validateToken() async {
    if (!_isAuthenticated) {
      return {
        'valid': false,
        'reason': 'Пользователь не авторизован',
        'shouldLogout': false,
      };
    }

    try {
      print('AuthProvider: Проверяем валидность токена...');
      final validToken = await SafeApiService.getValidToken();
      
      if (validToken == null) {
        print('AuthProvider: Токен недействителен, выполняем выход');
        await _logoutDueToInvalidSession('Сессия истекла');
        return {
          'valid': false,
          'reason': 'Сессия истекла',
          'shouldLogout': true,
        };
      }
      
      print('AuthProvider: Токен валиден');
      return {
        'valid': true,
        'reason': null,
        'shouldLogout': false,
      };
    } catch (e) {
      print('AuthProvider: Ошибка проверки токена: $e');
      await _logoutDueToInvalidSession('Ошибка проверки токена');
      return {
        'valid': false,
        'reason': 'Ошибка проверки токена',
        'shouldLogout': true,
      };
    }
  }

  Future<bool> updateProfile({
    required String firstName,
    required String lastName,
    required String email,
    required String phone,
    String? profilePicture,
    bool removeAvatar = false,
  }) async {
    if (_user == null) {
      print('AuthProvider: Пользователь не найден для обновления');
      return false;
    }

    print('AuthProvider: Начинаем обновление профиля');
    print('AuthProvider: Старые данные - ${_user!.firstName} ${_user!.lastName}, ${_user!.email}');
    print('AuthProvider: Новые данные - $firstName $lastName, $email');

    _isLoading = true;
    _error = null;
    notifyListeners();

    try {
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
        print('AuthProvider: Профиль успешно обновлен на сервере');
        
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

      print('AuthProvider: Обновленный пользователь создан');
      print('AuthProvider: Новый пользователь - ${_user!.firstName} ${_user!.lastName}, ${_user!.email}');

      // Сохраняем обновленный профиль локально
      await _saveUserToLocal(_user!);
      print('AuthProvider: Профиль сохранен локально успешно');

      _isLoading = false;
      notifyListeners();
      print('AuthProvider: notifyListeners() вызван');
      return true;
      } else {
        print('AuthProvider: Ошибка обновления профиля на сервере: ${result['error']}');
        _error = result['error'] ?? 'Ошибка обновления профиля';
        _isLoading = false;
        notifyListeners();
        return false;
      }
    } catch (e) {
      print('AuthProvider: Исключение при обновлении профиля: $e');
      _error = 'Ошибка обновления профиля: $e';
      _isLoading = false;
      notifyListeners();
      return false;
    }
  }
} 
 
 
 