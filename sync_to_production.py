#!/usr/bin/env python3
"""
Скрипт для синхронизации локального Django с продакшн сервером
"""

import os
import sys
import django
import requests
import json
from pathlib import Path

# Настройка Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maro.settings')
django.setup()

from core.models import Trip
from logistics.models import Task, Expense, Vehicle
from accounts.models import User

# Настройки продакшн сервера
PROD_API_BASE = 'https://barlau.org/api'
PROD_TOKEN = 'demo_token_for_web'  # Замените на реальный токен

def sync_trips():
    """Синхронизация заездов"""
    print("🔄 Синхронизация заездов...")
    
    # Получаем локальные заезды
    local_trips = Trip.objects.all()
    print(f"📊 Локальных заездов: {local_trips.count()}")
    
    for trip in local_trips:
        trip_data = {
            'id': trip.id,
            'vehicle': trip.vehicle.id if trip.vehicle else None,
            'driver': trip.driver.id if trip.driver else None,
            'status': trip.status,
            'start_address': trip.start_address,
            'end_address': trip.end_address,
            'cargo_description': trip.cargo_description,
            'cargo_weight': trip.cargo_weight,
            'planned_start_date': trip.planned_start_date.isoformat() if trip.planned_start_date else None,
            'planned_end_date': trip.planned_end_date.isoformat() if trip.planned_end_date else None,
        }
        
        try:
            # Отправляем на продакшн
            response = requests.post(
                f'{PROD_API_BASE}/trips/',
                headers={'Authorization': f'Bearer {PROD_TOKEN}'},
                json=trip_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Заезд {trip.id} синхронизирован")
            else:
                print(f"❌ Ошибка синхронизации заезда {trip.id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки заезда {trip.id}: {e}")

def sync_tasks():
    """Синхронизация задач"""
    print("🔄 Синхронизация задач...")
    
    # Получаем локальные задачи
    local_tasks = Task.objects.all()
    print(f"📊 Локальных задач: {local_tasks.count()}")
    
    for task in local_tasks:
        task_data = {
            'id': task.id,
            'title': task.title,
            'description': task.description,
            'priority': task.priority,
            'status': task.status,
            'due_date': task.due_date.isoformat() if task.due_date else None,
            'assigned_to': task.assigned_to.id if task.assigned_to else None,
            'created_by': task.created_by.id if task.created_by else None,
            'vehicle': task.vehicle.id if task.vehicle else None,
        }
        
        try:
            # Отправляем на продакшн
            response = requests.post(
                f'{PROD_API_BASE}/tasks/',
                headers={'Authorization': f'Bearer {PROD_TOKEN}'},
                json=task_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Задача {task.id} синхронизирована")
            else:
                print(f"❌ Ошибка синхронизации задачи {task.id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки задачи {task.id}: {e}")

def sync_expenses():
    """Синхронизация расходов"""
    print("🔄 Синхронизация расходов...")
    
    # Получаем локальные расходы
    local_expenses = Expense.objects.all()
    print(f"📊 Локальных расходов: {local_expenses.count()}")
    
    for expense in local_expenses:
        expense_data = {
            'id': expense.id,
            'description': expense.description,
            'amount': float(expense.amount),
            'category': expense.category,
            'date': expense.date.isoformat() if expense.date else None,
            'created_by': expense.created_by.id if expense.created_by else None,
            'vehicle': expense.vehicle.id if expense.vehicle else None,
        }
        
        try:
            # Отправляем на продакшн
            response = requests.post(
                f'{PROD_API_BASE}/expenses/',
                headers={'Authorization': f'Bearer {PROD_TOKEN}'},
                json=expense_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Расход {expense.id} синхронизирован")
            else:
                print(f"❌ Ошибка синхронизации расхода {expense.id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки расхода {expense.id}: {e}")

def sync_vehicles():
    """Синхронизация транспортных средств"""
    print("🔄 Синхронизация транспортных средств...")
    
    # Получаем локальные транспортные средства
    local_vehicles = Vehicle.objects.all()
    print(f"📊 Локальных транспортных средств: {local_vehicles.count()}")
    
    for vehicle in local_vehicles:
        vehicle_data = {
            'id': vehicle.id,
            'number': vehicle.number,
            'brand': vehicle.brand,
            'model': vehicle.model,
            'year': vehicle.year,
            'status': vehicle.status,
            'driver': vehicle.driver.id if vehicle.driver else None,
            'fuel_type': vehicle.fuel_type,
            'cargo_capacity': float(vehicle.cargo_capacity) if vehicle.cargo_capacity else None,
            'max_weight': float(vehicle.max_weight) if vehicle.max_weight else None,
            'description': vehicle.description,
            'vehicle_type': vehicle.vehicle_type,
            'vin_number': vehicle.vin_number,
            'engine_number': vehicle.engine_number,
            'chassis_number': vehicle.chassis_number,
            'engine_capacity': float(vehicle.engine_capacity) if vehicle.engine_capacity else None,
            'length': float(vehicle.length) if vehicle.length else None,
            'width': float(vehicle.width) if vehicle.width else None,
            'height': float(vehicle.height) if vehicle.height else None,
            'color': vehicle.color,
        }
        
        try:
            # Отправляем на продакшн
            response = requests.post(
                f'{PROD_API_BASE}/vehicles/',
                headers={'Authorization': f'Bearer {PROD_TOKEN}'},
                json=vehicle_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Транспортное средство {vehicle.id} синхронизировано")
            else:
                print(f"❌ Ошибка синхронизации транспортного средства {vehicle.id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки транспортного средства {vehicle.id}: {e}")

def sync_employees():
    """Синхронизация сотрудников"""
    print("🔄 Синхронизация сотрудников...")
    
    # Получаем локальных сотрудников
    local_employees = User.objects.filter(role__in=['DRIVER', 'DISPATCHER', 'MECHANIC', 'DIRECTOR', 'ACCOUNTANT'])
    print(f"📊 Локальных сотрудников: {local_employees.count()}")
    
    for employee in local_employees:
        employee_data = {
            'id': employee.id,
            'username': employee.username,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone': employee.phone,
            'role': employee.role,
            'is_active': employee.is_active,
            'hire_date': employee.hire_date.isoformat() if employee.hire_date else None,
        }
        
        try:
            # Отправляем на продакшн
            response = requests.post(
                f'{PROD_API_BASE}/employees/',
                headers={'Authorization': f'Bearer {PROD_TOKEN}'},
                json=employee_data
            )
            
            if response.status_code in [200, 201]:
                print(f"✅ Сотрудник {employee.id} синхронизирован")
            else:
                print(f"❌ Ошибка синхронизации сотрудника {employee.id}: {response.status_code}")
                
        except Exception as e:
            print(f"❌ Ошибка отправки сотрудника {employee.id}: {e}")

def main():
    """Основная функция синхронизации"""
    print("🚀 Начинаем синхронизацию с продакшн сервером...")
    print(f"📡 API: {PROD_API_BASE}")
    
    try:
        # Проверяем подключение к продакшн серверу
        response = requests.get(f'{PROD_API_BASE}/trips/', headers={'Authorization': f'Bearer {PROD_TOKEN}'})
        if response.status_code != 200:
            print(f"❌ Не удается подключиться к продакшн серверу: {response.status_code}")
            return
        
        print("✅ Подключение к продакшн серверу установлено")
        
        # Синхронизируем данные
        sync_trips()
        sync_tasks()
        sync_expenses()
        sync_vehicles()
        sync_employees()
        
        print("✅ Синхронизация завершена!")
        
    except Exception as e:
        print(f"❌ Ошибка синхронизации: {e}")

if __name__ == '__main__':
    main() 