# 📋 Инструкции по развертыванию изменений на сервер barlau.org

## 🔧 Данные для подключения
- **Сервер:** 85.202.192.33
- **Пользователь:** root
- **Пароль:** 33q97KKRfmnHTY6dCiyuA3g=
- **Директория проекта:** /var/www/barlau

## 🚀 Шаги развертывания

### 1. Подключение к серверу
```bash
ssh root@85.202.192.33
# Введите пароль: 33q97KKRfmnHTY6dCiyuA3g=
```

### 2. Переход в директорию проекта
```bash
cd /var/www/barlau
```

### 3. Получение изменений из GitHub
```bash
git fetch origin
git checkout mobile-menu-refactor
git pull origin mobile-menu-refactor
```

### 4. Перезапуск сервисов
```bash
systemctl reload nginx
systemctl restart barlau
```

### 5. Проверка статуса
```bash
systemctl status barlau
systemctl status nginx
```

## ✅ Проверка результата
После выполнения всех команд сайт должен быть доступен по адресу:
- **HTTP:** http://barlau.org
- **HTTPS:** https://barlau.org (если настроен SSL)

## 📝 Примененные изменения
1. ✅ **Центрирование текста в мобильном меню** - добавлен `text-center whitespace-nowrap`
2. ✅ **Поднятие мобильного меню** - добавлен `py-2`
3. ✅ **Удаление hover эффектов** - убраны `hover:text-blue-600`
4. ✅ **Скрытие бейджа уведомлений** - изменен `display: flex` на `display: none`
5. ✅ **Унификация высоты кнопок** - все кнопки имеют `padding: 16px 24px`

## 🔍 Файлы с изменениями
- `core/templates/core/dashboard.html`
- `core/templates/core/tasks.html`
- `core/templates/core/trucks.html`
- `core/templates/core/employees.html`
- `core/templates/core/map.html`
- И другие шаблоны с notif-badge

## 🎯 Коммит в GitHub
Все изменения зафиксированы в коммите: `a8da61f`
Ветка: `mobile-menu-refactor` 