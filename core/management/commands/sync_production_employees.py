from django.core.management.base import BaseCommand
from accounts.models import User
import requests
import json

class Command(BaseCommand):
    help = 'Синхронизирует данные сотрудников с продакшн сервера'

    def handle(self, *args, **options):
        try:
            # Загружаем данные с продакшн сервера
            response = requests.get(
                'https://barlau.org/api/employees/',
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                employees = data.get('results', [])
                
                self.stdout.write(f'Загружено {len(employees)} сотрудников с продакшн сервера')
                
                updated_count = 0
                for employee_data in employees:
                    try:
                        # Ищем пользователя по username
                        user = User.objects.get(username=employee_data['username'])
                        
                        # Обновляем поля
                        user.about_me = employee_data.get('about_me', '')
                        user.experience = employee_data.get('experience', '')
                        user.education = employee_data.get('education', '')
                        user.achievements = employee_data.get('achievements', '')
                        user.key_skills = employee_data.get('key_skills', '')
                        user.languages = employee_data.get('languages', '')
                        user.hobbies = employee_data.get('hobbies', '')
                        user.certifications = employee_data.get('certifications', '')
                        user.courses = employee_data.get('courses', '')
                        user.publications = employee_data.get('publications', '')
                        user.recommendations = employee_data.get('recommendations', '')
                        user.desired_salary = employee_data.get('desired_salary', '')
                        user.location = employee_data.get('location', '')
                        user.skype = employee_data.get('skype', '')
                        user.linkedin = employee_data.get('linkedin', '')
                        user.portfolio_url = employee_data.get('portfolio_url', '')
                        user.age = employee_data.get('age')
                        
                        user.save()
                        updated_count += 1
                        
                        self.stdout.write(
                            self.style.SUCCESS(f'Обновлен: {user.get_full_name()} ({user.username})')
                        )
                        
                    except User.DoesNotExist:
                        self.stdout.write(
                            self.style.WARNING(f'Пользователь не найден: {employee_data.get("username", "unknown")}')
                        )
                
                self.stdout.write(
                    self.style.SUCCESS(f'Успешно синхронизировано {updated_count} сотрудников')
                )
                
            else:
                self.stdout.write(
                    self.style.ERROR(f'Ошибка загрузки данных: {response.status_code}')
                )
                
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Ошибка синхронизации: {str(e)}')
            ) 