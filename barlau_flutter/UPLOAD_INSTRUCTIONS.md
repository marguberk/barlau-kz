# Инструкции для загрузки изменений на продакшн сервер

## Проблема
У нас есть проблемы с SSH подключением к серверу barlau.org. Нужно вручную загрузить следующие файлы:

## Файлы для загрузки

### 1. Django Views (core/views.py)
- **Локальный путь**: `/Users/almaty/cursors/maro/barlau_flutter/core/views.py`
- **Серверный путь**: `/var/www/barlau/core/views.py`
- **Изменения**: Добавлены классы `DriverDocumentsView` и `DriverDocumentDeleteView` в конец файла

### 2. Django URLs (core/urls.py)
- **Локальный путь**: `/Users/almaty/cursors/maro/barlau_flutter/core/urls.py`
- **Серверный путь**: `/var/www/barlau/core/urls.py`
- **Изменения**: Добавлены импорты и URL patterns для новых views

### 3. Шаблон формы сотрудника (core/templates/core/employee_form.html)
- **Локальный путь**: `/Users/almaty/cursors/maro/barlau_flutter/core/templates/core/employee_form.html`
- **Серверный путь**: `/var/www/barlau/core/templates/core/employee_form.html`
- **Изменения**: Добавлена секция "Документы водителя" с кнопкой "Управление документами"

### 4. Новый шаблон документов водителя (core/templates/core/driver_documents.html)
- **Локальный путь**: `/Users/almaty/cursors/maro/barlau_flutter/core/templates/core/driver_documents.html`
- **Серверный путь**: `/var/www/barlau/core/templates/core/driver_documents.html`
- **Изменения**: Новый файл для управления документами водителей

### 5. Flutter API Service (barlau_flutter/lib/services/safe_api_service.dart)
- **Локальный путь**: `/Users/almaty/cursors/maro/barlau_flutter/lib/services/safe_api_service.dart`
- **Серверный путь**: `/var/www/barlau/barlau_flutter/lib/services/safe_api_service.dart`
- **Изменения**: Исправлен импорт и метод `getDriverDocuments`

## Команды для загрузки

### Вариант 1: Через SCP (если SSH работает)
```bash
# Загрузить файлы по одному
scp core/views.py root@barlau.org:/var/www/barlau/core/
scp core/urls.py root@barlau.org:/var/www/barlau/core/
scp core/templates/core/employee_form.html root@barlau.org:/var/www/barlau/core/templates/core/
scp core/templates/core/driver_documents.html root@barlau.org:/var/www/barlau/core/templates/core/
scp barlau_flutter/lib/services/safe_api_service.dart root@barlau.org:/var/www/barlau/barlau_flutter/lib/services/
```

### Вариант 2: Через rsync (если SSH работает)
```bash
rsync -avz --exclude='.git' --exclude='node_modules' --exclude='__pycache__' --exclude='*.pyc' --exclude='.DS_Store' barlau_flutter/ root@barlau.org:/var/www/barlau/
```

### Вариант 3: Через веб-интерфейс или FTP
1. Подключиться к серверу через веб-интерфейс управления хостингом
2. Загрузить файлы через файловый менеджер

## После загрузки файлов

### 1. Перезапустить Django сервер
```bash
# На сервере
sudo systemctl restart gunicorn
sudo systemctl restart nginx
```

### 2. Применить миграции (если нужно)
```bash
# На сервере
cd /var/www/barlau
source venv/bin/activate
python manage.py makemigrations
python manage.py migrate
```

### 3. Проверить функциональность
1. Зайти на сайт https://barlau.org
2. Войти в систему
3. Перейти в "Сотрудники"
4. Выбрать любого водителя и нажать "Редактировать"
5. Проверить наличие секции "Документы водителя" с кнопкой "Управление документами"

## Что должно работать

1. **В форме редактирования сотрудника**: Для водителей должна появиться секция "Документы водителя" с кнопкой "Управление документами"

2. **Страница управления документами**: При нажатии на кнопку должна открыться страница с:
   - Формой для добавления новых документов
   - Списком существующих документов
   - Возможностью скачивания и удаления документов

3. **Типы документов**: Водительское удостоверение, Медицинская справка, Паспорт, Разрешение на работу, Страховка, Прочее

4. **Права доступа**: Только для ролей SUPERADMIN, DIRECTOR, DEPUTY_DIRECTOR, HR_MANAGER, ACCOUNTANT

## Тестирование

После загрузки файлов протестировать:
1. ✅ Кнопка "Управление документами" появляется для водителей
2. ✅ Страница документов открывается
3. ✅ Форма добавления документа работает
4. ✅ Документы сохраняются в базе данных
5. ✅ Файлы загружаются и скачиваются
6. ✅ Удаление документов работает


