# Руководство по развертыванию на PythonAnywhere

## Предварительная подготовка

1. Зарегистрируйтесь на [PythonAnywhere](https://www.pythonanywhere.com/) и приобретите платный аккаунт (например, Hacker за $12/месяц).
2. Проект готов к развертыванию, изменения залиты в GitHub.

## Шаги по развертыванию

### 1. Настройка веб-приложения

1. Войдите в свою учетную запись PythonAnywhere (barlaukz).
2. На панели управления перейдите во вкладку "Web".
3. Нажмите "Add a new web app".
4. Выберите свой домен (barlaukz.pythonanywhere.com).
5. Выберите "Manual configuration".
6. Выберите Python 3.10.
7. Нажмите "Next", чтобы завершить создание приложения.

### 2. Настройка базы данных MySQL

1. Перейдите на вкладку "Databases".
2. В разделе MySQL создайте новую базу данных:
   - Укажите пароль для администратора MySQL.
   - Создайте новую базу данных с именем `barlaukz$barlau`.

### 3. Настройка виртуального окружения и загрузка кода

1. Перейдите на вкладку "Consoles" и создайте новую Bash консоль.
2. Выполните следующие команды для создания виртуального окружения:

```bash
mkvirtualenv --python=python3.10 barlau
```

3. Клонируйте репозиторий из GitHub:

```bash
cd ~
git clone https://github.com/marguberk/barlau-kz.git
cd barlau-kz
```

4. Установите зависимости:

```bash
pip install -r requirements.txt
```

### 4. Настройка WSGI-файла

1. Вернитесь на вкладку "Web".
2. В разделе "Code" найдите WSGI configuration file, обычно по пути `/var/www/barlaukz_pythonanywhere_com_wsgi.py`.
3. Нажмите на этот файл, чтобы отредактировать его, и замените содержимое на следующее:

```python
import os
import sys

# Добавляем путь к проекту в sys.path
path = '/home/barlaukz/barlau-kz'
if path not in sys.path:
    sys.path.append(path)

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.pythonanywhere_settings')

application = get_wsgi_application()
```

4. Сохраните файл.

### 5. Настройка путей к статическим и медиа-файлам

1. В настройках веб-приложения (вкладка "Web"), перейдите к разделу "Static files".
2. Добавьте следующие пути:
   - URL: `/static/`, Directory: `/home/barlaukz/barlau-kz/staticfiles`
   - URL: `/media/`, Directory: `/home/barlaukz/barlau-kz/media`

### 6. Настройка переменных окружения

1. В том же разделе настроек веб-приложения найдите "Environment variables".
2. Добавьте необходимые переменные окружения, например:
   - `SECRET_KEY`: <secret_key>
   - `DEBUG`: False
   - `PYTHONANYWHERE_DOMAIN`: True

### 7. Миграция базы данных и сбор статических файлов

1. Вернитесь в консоль Bash.
2. Убедитесь, что вы находитесь в директории проекта и виртуальное окружение активировано:

```bash
cd ~/barlau-kz
workon barlau
```

3. Выполните миграции базы данных:

```bash
python manage.py migrate
```

4. Создайте суперпользователя:

```bash
python manage.py createsuperuser
```

5. Соберите статические файлы:

```bash
python manage.py collectstatic --noinput
```

### 8. Настройка разрешений на файлы и директории

1. Установите правильные разрешения для директорий media и staticfiles:

```bash
mkdir -p media
chmod 775 media
chmod 775 staticfiles
```

### 9. Перезапуск веб-приложения

1. Вернитесь на вкладку "Web".
2. Нажмите на кнопку "Reload" для перезапуска веб-приложения.

### 10. Проверка работоспособности

1. Перейдите по адресу [barlaukz.pythonanywhere.com](https://barlaukz.pythonanywhere.com).
2. Убедитесь, что приложение запущено и работает корректно.
3. Проверьте логи в разделе "Web" -> "Logs" в случае возникновения проблем.

## Устранение неполадок

### Ошибки при установке пакетов

Если возникают проблемы с установкой некоторых пакетов, попробуйте установить их с дополнительными опциями:

```bash
pip install weasyprint --no-deps
pip install mysqlclient --no-binary :all:
```

### Проблемы с базой данных

Если возникают проблемы с подключением к базе данных, проверьте настройки в файле `barlau/pythonanywhere_settings.py`:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "barlaukz$barlau",
        "USER": "barlaukz",
        "PASSWORD": "barlauhQ217$#",
        "HOST": "barlaukz.mysql.pythonanywhere-services.com",
        "PORT": "",
    }
}
```

### Проблемы со статическими файлами

Если статические файлы не загружаются, проверьте, что:
1. Пути к статическим файлам правильно настроены в настройках веб-приложения.
2. Команда `collectstatic` была выполнена успешно.
3. В настройках проекта `STATIC_URL` и `STATIC_ROOT` указаны правильно.

## Обновление приложения

Для обновления приложения после внесения изменений:

1. Подключитесь к консоли Bash.
2. Перейдите в директорию проекта:

```bash
cd ~/barlau-kz
workon barlau
```

3. Обновите код из GitHub:

```bash
git pull origin main
```

4. Установите новые зависимости (если есть):

```bash
pip install -r requirements.txt
```

5. Выполните миграции (если есть новые):

```bash
python manage.py migrate
```

6. Обновите статические файлы:

```bash
python manage.py collectstatic --noinput
```

7. Перезапустите веб-приложение через вкладку "Web" -> кнопка "Reload". 