# 🚀 Инструкция по деплою на barlau.org

## 📡 Подключение к серверу

```bash
ssh ubuntu@85.202.192.33
# Пароль: 33q97KKRfmnHTY6dCiyuA3g=
```

После подключения получите root права:
```bash
sudo -i
```

## 🔧 Автоматический деплой

1. **Скачайте и запустите deploy скрипт:**
```bash
wget https://raw.githubusercontent.com/marguberk/barlau-kz/local-version/deploy.sh
chmod +x deploy.sh
./deploy.sh
```

2. **Дождитесь завершения установки** (может занять 5-10 минут)

## 🌐 Проверка работы сайта

После завершения деплоя сайт будет доступен по адресу:
- **http://barlau.org**
- **http://www.barlau.org**

## 👤 Доступ к админке

- **URL:** http://barlau.org/admin/
- **Логин:** admin
- **Пароль:** admin123

## 📋 Полезные команды

### Управление приложением:
```bash
sudo systemctl status barlau      # Статус приложения
sudo systemctl restart barlau     # Перезапуск приложения
sudo systemctl stop barlau        # Остановка приложения
sudo systemctl start barlau       # Запуск приложения
```

### Управление веб-сервером:
```bash
sudo systemctl status nginx       # Статус Nginx
sudo systemctl restart nginx      # Перезапуск Nginx
sudo nginx -t                     # Тест конфигурации
```

### Логи:
```bash
sudo tail -f /var/log/nginx/error.log        # Логи ошибок Nginx
sudo tail -f /var/log/nginx/access.log       # Логи доступа Nginx
sudo journalctl -u barlau -f                 # Логи приложения
```

### Управление базой данных:
```bash
sudo -u postgres psql barlau_db   # Подключение к БД
```

## 🔄 Обновление приложения

Для обновления приложения после изменений в коде:

```bash
sudo su - barlau
cd barlau-kz
git pull origin local-version
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
exit
sudo systemctl restart barlau
```

## 🔒 Настройка HTTPS (опционально)

Установка SSL сертификата через Let's Encrypt:

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d barlau.org -d www.barlau.org
```

## 🛠️ Структура проекта на сервере

```
/home/barlau/barlau-kz/          # Основная директория проекта
├── venv/                        # Виртуальное окружение Python
├── static/                      # Статические файлы Django
├── media/                       # Загруженные пользователями файлы  
├── manage.py                    # Django manage script
└── barlau.sock                  # Unix socket для Gunicorn
```

## 🆘 Решение проблем

### Приложение не запускается:
```bash
sudo journalctl -u barlau -n 50  # Последние 50 строк логов
```

### Nginx показывает ошибку:
```bash
sudo nginx -t                    # Проверка конфигурации
sudo tail -f /var/log/nginx/error.log
```

### База данных недоступна:
```bash
sudo systemctl status postgresql
sudo -u postgres psql -l         # Список баз данных
```

## 📞 Поддержка

При возникновении проблем проверьте:
1. Статус всех сервисов
2. Логи приложения и Nginx
3. Права доступа к файлам
4. Подключение к базе данных

---
**Создано:** $(date)
**Версия:** local-version
**Сервер:** 85.202.192.33 (barlau.org) 