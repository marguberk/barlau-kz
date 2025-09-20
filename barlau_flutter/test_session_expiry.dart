#!/usr/bin/env dart
/**
 * Тест для проверки работы системы управления сессиями
 * Этот скрипт можно запустить для симуляции истечения токена
 */

import 'dart:io';
import 'dart:convert';

void main() async {
  print('🧪 Тест системы управления сессиями');
  print('=' * 50);
  
  // Проверяем текущее состояние
  await checkCurrentState();
  
  // Симулируем истечение токена
  await simulateTokenExpiry();
  
  print('\n✅ Тест завершен');
  print('\n📱 Теперь запустите приложение и проверьте:');
  print('   1. Показывается ли диалог "Сессия истекла"');
  print('   2. Перенаправляется ли пользователь на экран входа');
  print('   3. Очищаются ли все данные авторизации');
}

Future<void> checkCurrentState() async {
  print('🔍 Проверяем текущее состояние...');
  
  try {
    // Проверяем API напрямую
    final client = HttpClient();
    final request = await client.getUrl(
      Uri.parse('https://barlau.org/api/v1/users/me/')
    );
    
    final response = await request.close();
    print('API статус: ${response.statusCode}');
    
    if (response.statusCode == 200) {
      print('✅ API доступен');
    } else if (response.statusCode == 401 || response.statusCode == 403) {
      print('⚠️ API требует авторизации (${response.statusCode})');
    } else {
      print('❌ API недоступен (${response.statusCode})');
    }
    
    client.close();
  } catch (e) {
    print('❌ Ошибка проверки API: $e');
  }
}

Future<void> simulateTokenExpiry() async {
  print('\n🔄 Симулируем истечение токена...');
  
  // В реальном приложении токены хранятся в SharedPreferences
  // Мы не можем напрямую их изменить, но можем дать инструкции
  
  print('📝 Инструкции для тестирования:');
  print('   1. Откройте приложение');
  print('   2. Дождитесь истечения токена (обычно 24 часа)');
  print('   3. Или измените время на устройстве на +25 часов');
  print('   4. Попробуйте загрузить данные (расходы, задачи, грузовики)');
  print('   5. Должен появиться диалог "Сессия истекла"');
  print('   6. После нажатия "Понятно" должен открыться экран входа');
  
  print('\n🔧 Альтернативный способ тестирования:');
  print('   1. Запустите приложение');
  print('   2. Отключите интернет');
  print('   3. Попробуйте загрузить данные');
  print('   4. Включите интернет');
  print('   5. Попробуйте снова - должен появиться диалог об истечении сессии');
}








































