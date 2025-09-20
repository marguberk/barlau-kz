import 'dart:io';

void main() async {
  print('🔄 Исправление всех дублирований fontFamily...');
  
  // Список файлов для исправления
  final files = [
    'lib/screens/employees_screen.dart',
    'lib/screens/vehicles_screen.dart',
    'lib/screens/tasks_screen.dart',
    'lib/screens/trip_details_screen.dart',
    'lib/components/app_header.dart',
    'lib/components/web_image.dart',
    'lib/screens/profile_screen.dart',
    'lib/screens/expenses_screen.dart',
  ];
  
  for (final file in files) {
    await fixAllDuplicatesInFile(file);
  }
  
  print('✅ Исправление завершено!');
}

Future<void> fixAllDuplicatesInFile(String filePath) async {
  try {
    final file = File(filePath);
    if (!await file.exists()) {
      print('⚠️  Файл не найден: $filePath');
      return;
    }
    
    String content = await file.readAsString();
    int fixedCount = 0;
    
    // Исправляем дублирование fontFamily: 'InterTight', fontFamily: 'InterTight',
    final pattern1 = RegExp(r"fontFamily: 'InterTight',\s*fontFamily: 'InterTight'");
    final matches1 = pattern1.allMatches(content);
    
    for (final match in matches1.toList().reversed) {
      final before = content.substring(0, match.start);
      final after = content.substring(match.end);
      content = before + "fontFamily: 'InterTight'," + after;
      fixedCount++;
    }
    
    // Исправляем дублирование с отступами
    final pattern2 = RegExp(r"fontFamily: 'InterTight',\s*\n\s*fontFamily: 'InterTight'");
    final matches2 = pattern2.allMatches(content);
    
    for (final match in matches2.toList().reversed) {
      final before = content.substring(0, match.start);
      final after = content.substring(match.end);
      content = before + "fontFamily: 'InterTight'," + after;
      fixedCount++;
    }
    
    // Исправляем дублирование в одной строке
    final pattern3 = RegExp(r"fontFamily: 'InterTight',\s*fontFamily: 'InterTight',");
    final matches3 = pattern3.allMatches(content);
    
    for (final match in matches3.toList().reversed) {
      final before = content.substring(0, match.start);
      final after = content.substring(match.end);
      content = before + "fontFamily: 'InterTight'," + after;
      fixedCount++;
    }
    
    if (fixedCount > 0) {
      await file.writeAsString(content);
      print('✅ Исправлено $fixedCount дублирований в $filePath');
    } else {
      print('ℹ️  Нет дублирований в $filePath');
    }
    
  } catch (e) {
    print('❌ Ошибка исправления $filePath: $e');
  }
} 
 
 
 
 