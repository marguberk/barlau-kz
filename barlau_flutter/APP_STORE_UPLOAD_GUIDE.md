# 📱 Загрузка BARLAU в App Store

## ✅ Готовые файлы:
- **IPA файл**: `build/ios/ipa/barlau_flutter.ipa` (47.4 MB)
- **Версия**: 2.0.6 (Build 7) ✅ ИСПРАВЛЕНО!
- **Bundle ID**: kz.barlau.app.v2

## 🚀 Способы загрузки:

### Вариант 1: Через Xcode (Рекомендуется)
1. Откройте **Xcode**
2. Выберите **Window → Organizer**
3. Перейдите на вкладку **Archives**
4. Найдите архив **BARLAU Logistics** (версия 2.0.6)
5. Нажмите **Distribute App**
6. Выберите **App Store Connect**
7. Выберите **Upload**
8. Войдите в Apple ID: `marguberk@gmail.com`
9. Следуйте инструкциям

### Вариант 2: Через Apple Transporter
1. Скачайте **Transporter** из Mac App Store
2. Откройте Transporter
3. Перетащите файл `barlau_flutter.ipa` в Transporter
4. Войдите в Apple ID: `marguberk@gmail.com`
5. Нажмите **Deliver**

### Вариант 3: Через командную строку
```bash
# Нужен app-specific password для Apple ID
xcrun altool --upload-app \
  --type ios \
  -f build/ios/ipa/barlau_flutter.ipa \
  --username "marguberk@gmail.com" \
  --password "@your-app-specific-password"
```

## 📋 Что исправлено в этой версии:
- ✅ **Исправлено дублирование экрана PIN кода**
- ✅ **Плавная анимация перехода** от логина к PIN настройке
- ✅ **Единственный источник истины** для навигации
- ✅ **Стабильная работа** Touch ID/Face ID
- ✅ **Исправлены все черные экраны**
- ✅ **Улучшена производительность**

## 🔧 Настройки приложения:
- **Название**: BARLAU Logistics
- **Версия**: 2.0.6 ✅ ИСПРАВЛЕНО!
- **Build**: 7
- **Минимальная версия iOS**: 12.0
- **Поддерживаемые устройства**: iPhone, iPad
- **Размер**: ~47 MB

## 📝 Заметки:
- Приложение готово к публикации
- Все критические баги исправлены
- PIN код и биометрия работают корректно
- Анимации плавные и стабильные

## 🎯 Следующие шаги после загрузки:
1. Заполнить метаданные в App Store Connect
2. Добавить скриншоты
3. Настроить возрастной рейтинг
4. Отправить на модерацию
