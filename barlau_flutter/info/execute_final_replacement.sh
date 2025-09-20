#!/bin/bash

echo "🔄 Выполняем финальную замену данных в продакшн базе BARLAU.KZ"
echo "📅 Дата: $(date)"

# Параметры подключения
SERVER="85.202.192.33"
USER="ubuntu"
PASSWORD="33q97KKRfmnHTY6dCiyuA3g="

echo "🔌 Подключаемся к серверу $SERVER..."

# Выполняем финальную замену данных на сервере
sshpass -p "$PASSWORD" ssh -o StrictHostKeyChecking=no "$USER@$SERVER" << 'EOF'
# Создаем директорию для скриптов
mkdir -p /home/ubuntu/cleanup_scripts

# Создаем финальный Python скрипт замены данных
cat > /home/ubuntu/cleanup_scripts/final_data_replacement.py << 'PYTHON_EOF'
#!/usr/bin/env python3
import os
import sys
import django
from datetime import datetime

# Настройка Django
sys.path.append('/var/www/barlau')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'barlau.settings')
django.setup()

from accounts.models import User
from logistics.models import Vehicle
from django.db import transaction

def final_data_replacement():
    print("🔄 Начинаем финальную замену данных в продакшн базе...")
    print("📅 Дата: " + str(datetime.now()))
    
    with transaction.atomic():
        # ЭТАП 1: Очистка тестовых данных
        print("🧹 ЭТАП 1: Очистка тестовых данных...")
        
        # Удаляем тестовых пользователей (кроме админов) - используем raw SQL
        print("\n👥 Удаляем тестовых пользователей...")
        from django.db import connection
        cursor = connection.cursor()
        
        # Удаляем пользователей, которые не являются админами
        cursor.execute("""
            DELETE FROM accounts_user 
            WHERE role NOT IN ('SUPERADMIN', 'ADMIN', 'DIRECTOR')
        """)
        removed_users = cursor.rowcount
        print(f"  ❌ Удалено пользователей: {removed_users}")
        
        # Удаляем все транспортные средства
        print(f"\n🚛 Удаляем все транспортные средства...")
        cursor.execute("DELETE FROM logistics_vehicle")
        removed_vehicles = cursor.rowcount
        print(f"  ❌ Удалено ТС: {removed_vehicles}")
        
        # Удаляем связанные данные
        print(f"\n🧹 Очищаем связанные данные...")
        cursor.execute("DELETE FROM core_trip")
        trips_deleted = cursor.rowcount
        cursor.execute("DELETE FROM logistics_expense")
        expenses_deleted = cursor.rowcount
        print(f"  ❌ Удалено поездок: {trips_deleted}")
        print(f"  ❌ Удалено расходов: {expenses_deleted}")
        
        # ЭТАП 2: Добавление реальных данных
        print(f"\n📝 ЭТАП 2: Добавление реальных данных...")
        
        # Обновляем существующих администраторов
        print("\n👑 Обновляем информацию об администраторах...")
        
        # Беркинбаев Мейрлан Камалбекұлы
        cursor.execute("""
            UPDATE accounts_user 
            SET first_name = 'Мейрлан', 
                last_name = 'Беркинбаев',
                role = 'SUPERADMIN',
                phone = '+77777777777',
                email = 'admin@barlau.org',
                about_me = 'Руководитель компании BARLAU Truck Logistics',
                position = 'Руководитель'
            WHERE first_name LIKE '%Мейрлан%' AND last_name LIKE '%Беркинбаев%'
        """)
        print(f"  ✅ Обновлен: Беркинбаев Мейрлан Камалбекұлы")
        
        # Молдияров Аскар Ахатович
        cursor.execute("""
            UPDATE accounts_user 
            SET first_name = 'Аскар', 
                last_name = 'Молдияров',
                role = 'DIRECTOR',
                phone = '+77758881220',
                email = 'askar@barlau.org',
                about_me = 'Родился 20 декабря 1988 года в г. Караганда. Семейное положение-Женат. Окончил Российский Университет Дружбы Народов, г.Москва',
                position = 'Директор'
            WHERE first_name LIKE '%Аскар%' AND last_name LIKE '%Молдияров%'
        """)
        print(f"  ✅ Обновлен: Молдияров Аскар Ахатович")
        
        # Добавляем реальных сотрудников
        print(f"\n👥 Добавляем реальных сотрудников...")
        
        real_employees = [
            ('Серік', 'Айдарбеков', 'serik_aydarbekov', 'MANAGER', '+77757599686', 'serik@barlau.org', 'Родился 1 июня 1986 года. ИИН: 890601301168', 'Менеджер'),
            ('Алмасжан', 'Сопашев', 'almaszhan_sopashev', 'MANAGER', '+77057057876', 'almaszhan@barlau.org', 'Родился 24 декабря 1988 года в г.Жаркент. Семейное положение-Женат. Окончил Международный университет «Silkway». ИИН: 881224302564', 'Менеджер'),
            ('Мақсат', 'Құсайын', 'maksat_kusayin', 'MANAGER', '+77014977888', 'maksat@barlau.org', 'Родился 16 мая 1988 года в г.Жаркент. Семейное положение-Женат. ИИН: 880516300512', 'Менеджер'),
            ('Ерболат', 'Кудайбергенов', 'erbolat_kudaybergenov', 'MANAGER', '+77017525437', 'erbolat@barlau.org', 'Родился 25 февраля 1978 года с.Елтай, Ерейментауский р-он, Акмолинская область. ИИН: 780225350070', 'Менеджер'),
            ('Назерке', 'Садвакасова', 'nazerke_sadvakasova', 'ACCOUNTANT', '+77023200506', 'nazerke@barlau.org', 'Родилась 1 августа 1992 года в г.Жаркент. Семейное положение-Замужем. Окончила КазНУ', 'Бухгалтер'),
            ('Ғабит', 'Ахметов', 'gabit_akhmetov', 'TECH', '+77071778202', 'gabit@barlau.org', 'Родился 13 декабря 1990 года в г.Жаркент. Семейное положение-Холостой. ИИН: 901213302223', 'Техник'),
            ('Азиз', 'Илямов', 'aziz_ilyamov', 'TECH', '+777789509264', 'aziz@barlau.org', 'Родился 22 октября 1995 года в г.Жаркент. Семейное положение-Женат. ИИН: 951022300812', 'Техник'),
            ('Айдана', 'Ұзақ', 'aidana_uzak', 'MANAGER', '+77076156475', 'aidana@barlau.org', 'Родилась 1 февраля 1998 года в г.Жаркент. 2020 году окончила АТУ, по специальности-технология. Семейное положение-Замужем. Дети-1. ИИН: 980201400864', 'Менеджер'),
            ('Асель', 'Мұрат', 'asel_murat', 'MANAGER', '+777781008373', 'asel@barlau.org', 'Родилась 19 сентября 1995 года в г.Жаркент. Образование-незаконченное высшее. Семейное положение-в разводе. Дети-1. ИИН: 950919401325', 'Менеджер')
        ]
        
        added_employees = 0
        for emp_data in real_employees:
            try:
                cursor.execute("""
                    INSERT INTO accounts_user 
                    (username, first_name, last_name, email, role, phone, about_me, position, is_active, is_staff, is_superuser, password, date_joined, last_login, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, is_phone_verified, is_archived)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0, 'pbkdf2_sha256$600000$dummy$dummy', datetime('now'), NULL, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 0, 0)
                """, emp_data)
                added_employees += 1
                print(f"  ✅ Добавлен сотрудник: {emp_data[0]} {emp_data[1]} - {emp_data[3]}")
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении {emp_data[0]} {emp_data[1]}: {e}")
        
        # Добавляем реальных водителей
        print(f"\n🚗 Добавляем реальных водителей...")
        
        real_drivers = [
            ('Сухрат', 'Касимов', 'driver_sukhrat_kasimov', '+777775251777', '011001500617'),
            ('Хезиз', 'Қасенов', 'driver_kheziz_kassenov', '+77015843537', '900720302326'),
            ('Ғабит', 'Сабит', 'driver_gabit_sabit', '+77479499219', '990920300224'),
            ('Рустем', 'Садыров', 'driver_rustem_sadyrov', '+77054029789', '851015303223'),
            ('Хамражан', 'Пида', 'driver_khamrazhan_pida', '+77471676916', '940803300734'),
            ('Азизжан', 'Камердинов', 'driver_azizhan_kamerdinov', '+77477020048', '901026301546'),
            ('Сраилжан', 'Рузиев', 'driver_srailzhan_ruziev', '+77025432163', '900821301208'),
            ('Абдулжан', 'Саит', 'driver_abdulzhan_sait', '+777714592745', '950116300573'),
            ('Хамит', 'Абдуллаев', 'driver_khamit_abdullayev', '+77472506006', '930427301112'),
            ('Марат', 'Муталипов', 'driver_marat_mutalipov', '+777761605888', '880128302163'),
            ('Розахун', 'Исмаилов', 'driver_rozakhun_ismailov', '+777777242458', '970110300425'),
            ('Шахмурат', 'Касымов', 'driver_shakhmurat_kassymov', '+77079114708', '830828300014'),
            ('Жасулан', 'Кудайбергенов', 'driver_zhasulan_kudaybergenov', '+77052224788', '881204301349'),
            ('Елдос', 'Умурбеков', 'driver_yeldos_umurbekov', '+777759922900', '910405301367')
        ]
        
        added_drivers = 0
        for driver_data in real_drivers:
            try:
                cursor.execute("""
                    INSERT INTO accounts_user 
                    (username, first_name, last_name, email, role, phone, about_me, position, is_active, is_staff, is_superuser, password, date_joined, last_login, experience, education, skills, certifications, languages, desired_salary, location, skype, linkedin, portfolio_url, key_skills, achievements, courses, publications, recommendations, hobbies, is_phone_verified, is_archived)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, 1, 0, 0, 'pbkdf2_sha256$600000$dummy$dummy', datetime('now'), NULL, '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', '', 0, 0)
                """, (driver_data[2], driver_data[0], driver_data[1], f"{driver_data[0].lower()}@barlau.org", 'DRIVER', driver_data[3], f"Водительское удостоверение: {driver_data[4]}", 'Водитель'))
                added_drivers += 1
                print(f"  ✅ Добавлен водитель: {driver_data[0]} {driver_data[1]}")
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении водителя {driver_data[0]} {driver_data[1]}: {e}")
        
        # Добавляем реальные транспортные средства
        print(f"\n🚛 Добавляем реальные транспортные средства...")
        
        real_vehicles = [
            ('484ATL01', 'ВОЛЬВО', 'TRUCK'),
            ('057AUC01', 'ВОЛЬВО', 'TRUCK'),
            ('456AUC01', 'ВОЛЬВО', 'TRUCK'),
            ('956AUN01', 'ВОЛЬВО', 'TRUCK'),
            ('533ATL01', 'ВОЛЬВО', 'TRUCK'),
            ('290ATL01', 'ВОЛЬВО', 'TRUCK'),
            ('355ATL01', 'ВОЛЬВО', 'TRUCK'),
            ('474ATL01', 'ВОЛЬВО', 'TRUCK'),
            ('257ASC01', 'ВОЛЬВО', 'TRUCK'),
            ('108AGR19', 'ВОЛЬВО', 'TRUCK'),
            ('481ACA19', 'ВОЛЬВО', 'TRUCK'),
            ('523BMT02', 'ВОЛЬВО', 'TRUCK'),
            ('042BJK02', 'ВОЛЬВО', 'TRUCK'),
            ('695BHS02', 'ВОЛЬВО', 'TRUCK'),
            ('213AUL01', 'МЕРСЕДЕС', 'TRUCK'),
            ('208AUL01', 'МЕРСЕДЕС', 'TRUCK'),
            ('203AUL01', 'МЕРСЕДЕС', 'TRUCK'),
            ('359AUL01', 'МЕРСЕДЕС', 'TRUCK'),
            ('355AUL01', 'МЕРСЕДЕС', 'TRUCK'),
            ('287AUL01', 'КАМАЗ', 'TRUCK'),
            ('917AQM01', 'КАМАЗ', 'TRUCK'),
            ('913AQM01', 'КАМАЗ', 'TRUCK'),
            ('105AGR19', 'КАМАЗ', 'TRUCK'),
            ('494AVW01', 'DAF', 'TRUCK')
        ]
        
        added_vehicles = 0
        for vehicle_data in real_vehicles:
            try:
                cursor.execute("""
                    INSERT INTO logistics_vehicle 
                    (number, brand, model, year, status, vehicle_type, created_at, updated_at, cargo_capacity, fuel_type, is_archived)
                    VALUES (?, ?, ?, 2020, 'AVAILABLE', ?, datetime('now'), datetime('now'), 20.0, 'DIESEL', 0)
                """, vehicle_data)
                added_vehicles += 1
                print(f"  ✅ Добавлено ТС: {vehicle_data[0]} - {vehicle_data[1]}")
            except Exception as e:
                print(f"  🔴 Ошибка при добавлении ТС {vehicle_data[0]}: {e}")
        
        print(f"\n🎉 Финальная замена данных завершена!")
        print(f"📊 Статистика операции:")
        print(f"  ❌ Удалено пользователей: {removed_users}")
        print(f"  ❌ Удалено ТС: {removed_vehicles}")
        print(f"  ✅ Добавлено сотрудников: {added_employees}")
        print(f"  ✅ Добавлено водителей: {added_drivers}")
        print(f"  ✅ Добавлено ТС: {added_vehicles}")
        
        # Получаем итоговую статистику
        cursor.execute("SELECT COUNT(*) FROM accounts_user")
        total_users = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM logistics_vehicle")
        total_vehicles = cursor.fetchone()[0]
        
        print(f"\n📈 Итоговая статистика базы данных:")
        print(f"  👤 Пользователей: {total_users}")
        print(f"  🚛 Транспортных средств: {total_vehicles}")

if __name__ == "__main__":
    final_data_replacement()
PYTHON_EOF

# Переходим в директорию проекта
cd /var/www/barlau

# Активируем виртуальное окружение
source venv/bin/activate

# Создаем резервную копию
echo "💾 Создаем резервную копию базы данных..."
BACKUP_FILE="backup_before_final_replacement_$(date +%Y%m%d_%H%M%S).sqlite3"
cp db.sqlite3 "/home/ubuntu/backups/$BACKUP_FILE"
echo "✅ Резервная копия создана: $BACKUP_FILE"

# Выполняем финальную замену данных
echo "🔄 Выполняем финальную замену данных..."
python /home/ubuntu/cleanup_scripts/final_data_replacement.py

echo "✅ Финальная замена данных завершена!"
EOF

echo ""
echo "🎉 Финальная замена данных в продакшн базе завершена!"
echo "📅 Время завершения: $(date)"
