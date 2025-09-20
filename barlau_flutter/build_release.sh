#!/bin/bash

echo "🚀 Сборка релизных версий BARLAU.KZ"
echo "=================================="

# Очистка предыдущих сборок
echo "🧹 Очистка предыдущих сборок..."
flutter clean

# Получение зависимостей
echo "📦 Получение зависимостей..."
flutter pub get

# Генерация иконок
echo "🎨 Генерация иконок..."
flutter pub run flutter_launcher_icons:main

# Сборка Android APK
echo "🤖 Сборка Android APK..."
flutter build apk --release

# Сборка Android App Bundle (для Google Play)
echo "📱 Сборка Android App Bundle..."
flutter build appbundle --release

# Сборка iOS (только если на macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    echo "🍎 Сборка iOS..."
    flutter build ios --release --no-codesign
    echo "✅ iOS сборка завершена (без подписи)"
else
    echo "⚠️  iOS сборка пропущена (требуется macOS)"
fi

echo ""
echo "✅ Сборка завершена!"
echo ""
echo "📁 Файлы для публикации:"
echo "   Android APK: build/app/outputs/flutter-apk/app-release.apk"
echo "   Android Bundle: build/app/outputs/bundle/release/app-release.aab"
echo ""
echo "📋 Следующие шаги:"
echo "   1. Google Play Store: загрузите app-release.aab"
echo "   2. Apple App Store: откройте ios/Runner.xcworkspace в Xcode"
echo "   3. Настройте подпись и загрузите через Xcode"
echo ""
echo "🔐 Keystore информация:"
echo "   Файл: android/app/upload-keystore.jks"
echo "   Пароль: barlau2024"
echo "   Алиас: upload" 
# Сборка APK (для тестирования)
echo "🤖 Сборка APK..."
flutter build apk --release

if [ $? -eq 0 ]; then
    echo "✅ APK собран успешно!"
    echo "📁 Файл: build/app/outputs/flutter-apk/app-release.apk"
else
    echo "❌ Ошибка при сборке APK"
    exit 1
fi

# Информация о файлах
echo ""
echo "📊 Информация о собранных файлах:"
if [ -f "build/app/outputs/bundle/release/app-release.aab" ]; then
    AAB_SIZE=$(du -h build/app/outputs/bundle/release/app-release.aab | cut -f1)
    echo "   📦 App Bundle: $AAB_SIZE (для Google Play Store)"
fi

if [ -f "build/app/outputs/flutter-apk/app-release.apk" ]; then
    APK_SIZE=$(du -h build/app/outputs/flutter-apk/app-release.apk | cut -f1)
    echo "   📱 APK: $APK_SIZE (для тестирования)"
fi

echo ""
echo "🎉 Сборка завершена успешно!"
echo ""
echo "📋 Следующие шаги:"
echo "1. Загрузите app-release.aab в Google Play Console"
echo "2. Протестируйте app-release.apk на Android устройстве"
echo "3. Следуйте инструкциям в STORE_DEPLOYMENT_GUIDE.md" 