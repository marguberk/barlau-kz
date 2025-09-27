import 'dart:convert';
import 'dart:io';
import 'package:http/http.dart' as http;
import 'package:shared_preferences/shared_preferences.dart';
import '../config/app_config.dart';

class SafeApiService {
  static String get prodUrl => AppConfig.baseApiUrl;
  static const Duration timeout = Duration(seconds: 5);
  
  // Безопасный HTTP запрос с таймаутом
  static Future<Map<String, dynamic>> safeRequest(
    String endpoint, {
    String method = 'GET',
    Map<String, dynamic>? body,
    Map<String, String>? headers,
  }) async {
    try {
      final uri = Uri.parse('${AppConfig.baseApiUrl}$endpoint');
      print('🌐 SafeAPI Request: $method $uri');
      
      final defaultHeaders = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        ...?headers,
      };
      
      http.Response response;
      
      switch (method.toUpperCase()) {
        case 'POST':
          response = await http.post(
            uri,
            headers: defaultHeaders,
            body: body != null ? jsonEncode(body) : null,
          ).timeout(timeout);
          break;
        case 'PUT':
          response = await http.put(
            uri,
            headers: defaultHeaders,
            body: body != null ? jsonEncode(body) : null,
          ).timeout(timeout);
          break;
        case 'DELETE':
          response = await http.delete(
            uri,
            headers: defaultHeaders,
          ).timeout(timeout);
          break;
        default:
          response = await http.get(
            uri,
            headers: defaultHeaders,
          ).timeout(timeout);
      }
      
      print('🌐 SafeAPI Response: ${response.statusCode}');
      
      if (response.statusCode >= 200 && response.statusCode < 300) {
        final data = response.body.isNotEmpty 
            ? jsonDecode(response.body) 
            : {};
        return {
          'success': true,
          'data': data,
          'statusCode': response.statusCode,
        };
      } else {
        return {
          'success': false,
          'error': 'HTTP ${response.statusCode}',
          'statusCode': response.statusCode,
        };
      }
    } catch (e) {
      print('🔴 SafeApiService: Ошибка запроса к $endpoint - $e');
      return {
        'success': false,
        'error': 'Ошибка сети: $e',
        'statusCode': 0,
      };
    }
  }
  
  // Проверка доступности сервера
  static Future<bool> isServerAvailable() async {
    try {
      final result = await safeRequest('/vehicles/', headers: {'timeout': '3'});
      return result['success'] == true;
    } catch (e) {
      return false;
    }
  }
  
  // Проверка валидности токена
  static Future<Map<String, dynamic>> validateToken(String token) async {
    try {
      print('SafeApiService: Проверяем валидность токена...');
      final result = await safeRequest('/v1/users/me/', 
        headers: {
          'Authorization': 'Bearer $token',
        },
      );
      
      if (result['success'] && result['data'] != null) {
        print('SafeApiService: Токен валиден');
        return {
          'success': true,
          'data': result['data'],
        };
      } else {
        print('SafeApiService: Токен невалиден');
        return {
          'success': false,
          'error': 'Токен невалиден',
        };
      }
    } catch (e) {
      print('SafeApiService: Ошибка проверки токена: $e');
      return {
        'success': false,
        'error': 'Ошибка проверки токена: $e',
      };
    }
  }
  
  // Безопасная авторизация
  static Future<Map<String, dynamic>> safeLogin(String username, String password) async {
    try {
      print('SafeApiService: Попытка входа для $username');
      
      // Сначала проверяем, не валиден ли уже существующий токен
      final prefs = await SharedPreferences.getInstance();
      final existingToken = prefs.getString('auth_token');
      
      if (existingToken != null) {
        print('SafeApiService: Найден существующий токен, проверяем его валидность...');
        final tokenValidation = await validateToken(existingToken);
        if (tokenValidation['success']) {
          print('SafeApiService: Существующий токен валиден, используем его');
          return {
            'success': true,
            'data': {
              'access': existingToken,
              'refresh': prefs.getString('refresh_token'),
              'user': tokenValidation['data'],
            }
          };
        } else {
          print('SafeApiService: Существующий токен невалиден, выполняем новую авторизацию');
        }
      }
      
      print('SafeApiService: URL авторизации: ${AppConfig.baseApiUrl}/v1/auth/token/');
      
      // Выполняем новую авторизацию
      final result = await safeRequest('/v1/auth/token/', 
        method: 'POST',
        body: {
          'username': username,
          'password': password,
        },
      );
      
      print('SafeApiService: Результат авторизации: ${result['success']}');
      print('SafeApiService: Статус код: ${result['statusCode']}');
      if (result['data'] != null) {
        print('SafeApiService: Данные ответа: ${result['data']}');
      }
      
      if (result['success'] && result['data'] != null) {
        print('SafeApiService: Успешная авторизация через API');
        
        final tokenData = result['data'];
        final accessToken = tokenData['access'];
        final refreshToken = tokenData['refresh'];
        
        print('SafeApiService: Access token получен: ${accessToken != null ? 'да' : 'нет'}');
        print('SafeApiService: Refresh token получен: ${refreshToken != null ? 'да' : 'нет'}');
        
        if (accessToken != null) {
          // Сохраняем токены
          final prefs = await SharedPreferences.getInstance();
          await prefs.setString('auth_token', accessToken);
          await prefs.setString('refresh_token', refreshToken);
          
          print('SafeApiService: Реальный токен сохранен: ${accessToken.substring(0, 20)}...');
          
          // Получаем данные пользователя
          print('SafeApiService: Получаем данные пользователя...');
          final userResult = await safeRequest('/v1/users/me/', 
            headers: {
              'Authorization': 'Bearer $accessToken',
            },
          );
          
          print('SafeApiService: Результат получения данных пользователя: ${userResult['success']}');
          print('SafeApiService: Статус код пользователя: ${userResult['statusCode']}');
          
          if (userResult['success'] && userResult['data'] != null) {
            final userData = userResult['data'];
            await prefs.setString('user_profile', jsonEncode(userData));
            await prefs.setString('user_role', userData['role'] ?? '');
            await prefs.setInt('user_id', userData['id'] ?? 0);
            
            print('SafeApiService: Данные пользователя сохранены - роль: ${userData['role']}');
            print('SafeApiService: ID пользователя: ${userData['id']}');
            print('SafeApiService: Имя пользователя: ${userData['first_name']} ${userData['last_name']}');
            print('SafeApiService: Фото пользователя: ${userData['photo']}');
            
            return {
              'success': true,
              'data': {
                'user': userData,
              },
            };
          } else {
            print('SafeApiService: Ошибка получения данных пользователя: ${userResult['error']}');
            return {
              'success': false,
              'error': 'Ошибка получения данных пользователя',
            };
          }
        } else {
          print('SafeApiService: Токен не найден в ответе');
          return {
            'success': false,
            'error': 'Токен авторизации не найден',
          };
        }
      } else {
        print('SafeApiService: Ошибка авторизации через API: ${result['error']}');
        
        // Убираем демо-режим - только реальная авторизация
        print('SafeApiService: Ошибка авторизации через API: ${result['error']}');
        
              return {
        'success': false,
        'error': 'Неверный логин или пароль. Проверьте правильность введенных данных.',
      };
      }
    } catch (e) {
      print('SafeApiService: Ошибка авторизации: $e');
      
      // Убираем демо-режим - только реальная авторизация
      print('SafeApiService: Ошибка сети при авторизации: $e');
      
      return {
        'success': false,
        'error': 'Ошибка сети: $e',
      };
    }
  }
  
  // Безопасная загрузка данных с fallback
  static Future<Map<String, dynamic>> safeLoadData(
    String endpoint, {
    Map<String, dynamic>? fallbackData,
    String? authToken,
  }) async {
    try {
      // Проверяем доступность сервера
      final isAvailable = await isServerAvailable();
      
      if (!isAvailable) {
        print('SafeApiService: Сервер недоступен, используем fallback данные');
        return {
          'success': true,
          'data': fallbackData,
          'source': 'fallback',
          'warning': 'Сервер недоступен, используются тестовые данные',
        };
      }
      
      // Загружаем данные с сервера
      final headers = <String, String>{};
      if (authToken != null) {
        headers['Authorization'] = 'Bearer $authToken';
      }
      
      final result = await safeRequest(endpoint, headers: headers);
      
      if (result['success']) {
        return {
          'success': true,
          'data': result['data'],
          'source': 'server',
        };
      } else {
        print('SafeApiService: Ошибка загрузки данных: ${result['error']}');
        return {
          'success': true,
          'data': fallbackData,
          'source': 'fallback',
          'warning': 'Сервер недоступен, используются тестовые данные',
        };
      }
    } catch (e) {
      print('SafeApiService: Ошибка загрузки данных: $e');
      return {
        'success': true,
        'data': fallbackData,
        'source': 'fallback',
        'warning': 'Сервер недоступен, используются тестовые данные',
      };
    }
  }

  // Обновление профиля пользователя
  static Future<Map<String, dynamic>> updateUserProfile({
    required String firstName,
    required String lastName,
    required String email,
    required String phone,
    String? profilePicture,
    bool removeAvatar = false,
  }) async {
    try {
      print('SafeApiService: Обновление профиля пользователя');
      
      // Получаем токен авторизации
      final prefs = await SharedPreferences.getInstance();
      final token = prefs.getString('auth_token');
      
      if (token == null) {
        return {
          'success': false,
          'error': 'Токен авторизации не найден',
        };
      }

      // Подготавливаем данные для отправки
      final updateData = <String, dynamic>{
        'first_name': firstName,
        'last_name': lastName,
        'email': email,
        'phone': phone,
      };

      if (removeAvatar) {
        updateData['photo'] = null;
      } else if (profilePicture != null) {
        // Загружаем фото как файл
        try {
          final file = File(profilePicture);
          if (await file.exists()) {
            final bytes = await file.readAsBytes();
            final base64Image = base64Encode(bytes);
            // Определяем расширение файла
            final extension = profilePicture.split('.').last.toLowerCase();
            final mimeType = extension == 'jpg' || extension == 'jpeg' 
                ? 'image/jpeg' 
                : extension == 'png' 
                    ? 'image/png' 
                    : 'image/jpeg';
            updateData['photo'] = 'data:$mimeType;base64,$base64Image';
            print('SafeApiService: Фото загружено и закодировано в base64');
          } else {
            print('SafeApiService: Файл фото не найден: $profilePicture');
          }
        } catch (e) {
          print('SafeApiService: Ошибка загрузки фото: $e');
        }
      }

      print('SafeApiService: Отправляем данные: $updateData');

      // Отправляем запрос на обновление профиля
      final result = await safeRequest('/v1/users/me/', 
        method: 'PUT',
        headers: {
          'Authorization': 'Bearer $token',
        },
        body: updateData,
      );

      if (result['success'] && result['data'] != null) {
        print('SafeApiService: Профиль успешно обновлен на сервере');
        
        // Обновляем локальные данные пользователя
        await prefs.setString('user_profile', jsonEncode(result['data']));
        
        return {
          'success': true,
          'data': result['data'],
        };
      } else {
        print('SafeApiService: Ошибка обновления профиля: ${result['error']}');
        return {
          'success': false,
          'error': result['error'] ?? 'Ошибка обновления профиля',
        };
      }
    } catch (e) {
      print('SafeApiService: Ошибка обновления профиля: $e');
      return {
        'success': false,
        'error': 'Ошибка сети: $e',
      };
    }
  }

  // Обновление токена авторизации
  static Future<Map<String, dynamic>> refreshAuthToken() async {
    try {
      print('SafeApiService: Попытка обновления токена...');
      
      final prefs = await SharedPreferences.getInstance();
      final refreshToken = prefs.getString('refresh_token');
      
      if (refreshToken == null) {
        print('SafeApiService: Refresh токен не найден');
        return {
          'success': false,
          'error': 'Refresh токен не найден',
        };
      }

      final result = await safeRequest('/v1/auth/token/refresh/', 
        method: 'POST',
        body: {
          'refresh': refreshToken,
        },
      );

      if (result['success'] && result['data'] != null) {
        final tokenData = result['data'];
        final newAccessToken = tokenData['access'];
        
        if (newAccessToken != null) {
          // Сохраняем новый токен
          await prefs.setString('auth_token', newAccessToken);
          
          print('SafeApiService: Токен успешно обновлен: ${newAccessToken.substring(0, 20)}...');
          
          return {
            'success': true,
            'data': {
              'access_token': newAccessToken,
            },
          };
        } else {
          print('SafeApiService: Новый токен не найден в ответе');
          return {
            'success': false,
            'error': 'Новый токен не найден',
          };
        }
      } else {
        print('SafeApiService: Ошибка обновления токена: ${result['error']}');
        return {
          'success': false,
          'error': 'Ошибка обновления токена',
        };
      }
    } catch (e) {
      print('SafeApiService: Ошибка обновления токена: $e');
      return {
        'success': false,
        'error': 'Ошибка сети: $e',
      };
    }
  }

  // Принудительное обновление токена
  static Future<String?> forceRefreshToken() async {
    try {
      print('SafeApiService: Принудительное обновление токена...');
      
      final refreshResult = await refreshAuthToken();
      if (refreshResult['success']) {
        print('SafeApiService: Токен успешно обновлен принудительно');
        return refreshResult['data']['access_token'];
      } else {
        print('SafeApiService: Не удалось обновить токен принудительно');
        return null;
      }
    } catch (e) {
      print('SafeApiService: Ошибка принудительного обновления токена: $e');
      return null;
    }
  }

  // Получение валидного токена (с автоматическим обновлением)
  static Future<String?> getValidToken() async {
    try {
      final prefs = await SharedPreferences.getInstance();
      String? token = prefs.getString('auth_token');
      
      if (token == null) {
        print('SafeApiService: Токен не найден');
        return null;
      }

      // Проверяем, не истек ли токен, пытаясь сделать тестовый запрос
      final testResult = await safeRequest('/v1/users/me/', 
        headers: {
          'Authorization': 'Bearer $token',
        },
      );

      if (testResult['success']) {
        print('SafeApiService: Токен валиден');
        return token;
      } else if (testResult['statusCode'] == 401 || testResult['statusCode'] == 403) {
        print('SafeApiService: Токен истек (${testResult['statusCode']}), пытаемся обновить...');
        
        final refreshResult = await refreshAuthToken();
        if (refreshResult['success']) {
          print('SafeApiService: Токен успешно обновлен');
          return refreshResult['data']['access_token'];
        } else {
          print('SafeApiService: Не удалось обновить токен - сессия истекла');
          // Очищаем все токены при неудачном обновлении
          await prefs.remove('auth_token');
          await prefs.remove('refresh_token');
          return null;
        }
      } else {
        print('SafeApiService: Ошибка проверки токена: ${testResult['error']}');
        return token; // Возвращаем токен, даже если есть другие ошибки
      }
    } catch (e) {
      print('SafeApiService: Ошибка получения валидного токена: $e');
      return null;
    }
  }
  
  /// Обновление местоположения пользователя
  static Future<bool> updateUserLocation({
    required double latitude,
    required double longitude,
  }) async {
    try {
      final token = await getValidToken();
      if (token == null) {
        print('SafeApiService: Нет токена для обновления местоположения');
        return false;
      }
      
      final result = await safeRequest(
        '/v1/users/me/location/',
        method: 'PATCH',
        body: {
          'current_latitude': latitude,
          'current_longitude': longitude,
        },
        headers: {
          'Authorization': 'Bearer $token',
        },
      );
      
      if (result['success'] && result['statusCode'] == 200) {
        print('SafeApiService: Местоположение успешно обновлено');
        return true;
      } else {
        print('SafeApiService: Ошибка обновления местоположения: ${result['error']}');
        return false;
      }
    } catch (e) {
      print('SafeApiService: Ошибка обновления местоположения: $e');
      return false;
    }
  }

  // Получение документов водителя
  static Future<List<Map<String, dynamic>>?> getDriverDocuments({
    int? driverId,
  }) async {
    try {
      final token = await getValidToken();
      if (token == null) {
        print('SafeApiService: Нет токена для загрузки документов водителя');
        return null;
      }

      String endpoint = '/v1/driver-documents/';
      if (driverId != null) {
        endpoint += '?driver_id=$driverId';
      }

      print('SafeApiService: Загружаем документы водителя с endpoint: $endpoint');

      final result = await safeRequest(
        endpoint,
        headers: {
          'Authorization': 'Bearer $token',
        },
      );

      print('SafeApiService: Документы водителя - статус: ${result['statusCode']}');

      if (result['success'] && result['data'] != null) {
        final data = result['data'];
        if (data is List) {
          return List<Map<String, dynamic>>.from(data);
        } else if (data is Map && data.containsKey('results')) {
          return List<Map<String, dynamic>>.from(data['results']);
        }
        return null;
      } else {
        print('SafeApiService: Ошибка загрузки документов водителя: ${result['error']}');
        return null;
      }
    } catch (e) {
      print('SafeApiService: Исключение при загрузке документов водителя: $e');
      return null;
    }
  }

  // Получение детальных данных сотрудника
  static Future<Map<String, dynamic>> getEmployeeDetails(int employeeId) async {
    try {
      final token = await getValidToken();
      if (token == null) {
        throw Exception('Токен авторизации не найден');
      }

      final response = await safeRequest(
        '/v1/users/$employeeId/',
        headers: {
          'Authorization': 'Bearer $token',
        },
      );

      print('SafeApiService: Детальные данные сотрудника - статус: ${response['_status']}');
      return response;
    } catch (e) {
      print('SafeApiService: Ошибка загрузки детальных данных сотрудника: $e');
      rethrow;
    }
  }
}