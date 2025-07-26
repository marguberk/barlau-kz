from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Заполняет данные сотрудников (биография, образование, достижения)'

    def handle(self, *args, **options):
        # Данные для заполнения
        employee_data = {
            'admin': {
                'about_me': 'Супер администратор системы с полным доступом ко всем функциям.',
                'experience': 'Более 10 лет опыта в IT и системном администрировании.',
                'education': 'Высшее техническое образование, сертификации по безопасности.',
                'achievements': 'Внедрение и поддержка корпоративных систем управления.',
            },
            'dispatcher': {
                'about_me': 'Опытный диспетчер с отличными навыками координации и планирования.',
                'experience': '5+ лет в логистике и диспетчеризации.',
                'education': 'Логистический колледж, курсы по управлению транспортом.',
                'achievements': 'Оптимизация маршрутов на 30%, снижение простоев на 25%.',
            },
            'arman': {
                'about_me': 'Профессиональный водитель международных рейсов с безупречной репутацией.',
                'experience': '8 лет вождения грузовых автомобилей.',
                'education': 'Автотранспортный колледж, категория E.',
                'achievements': 'Более 500,000 км без аварий, водитель года 2023.',
            },
            'muratjan.ilakhunov': {
                'about_me': 'Консультант по развитию бизнеса и стратегическому планированию.',
                'experience': '12 лет консалтинга в различных отраслях.',
                'education': 'КИМЭП, MBA, сертификации по управлению проектами.',
                'achievements': 'Консультирование 20+ компаний, рост прибыли клиентов на 40%.',
            },
            'gabit.akhmetov': {
                'about_me': 'Специалист по закупкам и управлению складскими запасами.',
                'experience': '7 лет в сфере снабжения и логистики.',
                'education': 'Торгово-экономический институт, курсы по закупкам.',
                'achievements': 'Снижение затрат на закупки на 20%, оптимизация складских запасов.',
            },
            'aidana.uzakova': {
                'about_me': 'Специалист по планированию маршрутов и координации поставок.',
                'experience': '6 лет в логистике и координации.',
                'education': 'КазЭУ им. Т. Рыскулова, логистика.',
                'achievements': 'Оптимизация маршрутов на 25%, улучшение клиентского сервиса.',
            },
            'erbolat.kudaibergenov': {
                'about_me': 'Менеджер по работе с клиентами и развитию партнерских отношений.',
                'experience': '9 лет в продажах и клиентском сервисе.',
                'education': 'АТУ, менеджмент, курсы по продажам.',
                'achievements': 'Привлечение 15+ новых клиентов, рост продаж на 35%.',
            },
            'nazerke.sadvakasova': {
                'about_me': 'Главный бухгалтер с опытом ведения учета в транспортных компаниях.',
                'experience': '10 лет в бухгалтерии и финансовом учете.',
                'education': 'КазЭУ, учет и аудит, сертификации по МСФО.',
                'achievements': 'Безупречная отчетность 5+ лет, оптимизация налоговых платежей.',
            },
            'maksat.kusaiyn': {
                'about_me': 'Руководитель IT-отдела, отвечает за цифровизацию процессов.',
                'experience': '8 лет в IT и системной интеграции.',
                'education': 'КазНТУ, информационные системы, сертификации Microsoft.',
                'achievements': 'Внедрение CRM и ERP систем, автоматизация 80% процессов.',
            },
            'yunus.aliev': {
                'about_me': 'Опытный водитель дальних рейсов, специализация на международных перевозках.',
                'experience': '12 лет вождения, специализация на европейских маршрутах.',
                'education': 'Автошкола категории E, курсы по международным перевозкам.',
                'achievements': 'Водитель года 2023, безаварийное вождение 10+ лет.',
            },
        }

        updated_count = 0
        
        for username, data in employee_data.items():
            try:
                user = User.objects.get(username=username)
                user.about_me = data['about_me']
                user.experience = data['experience']
                user.education = data['education']
                user.achievements = data['achievements']
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Обновлен сотрудник: {user.get_full_name()}')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Сотрудник не найден: {username}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно обновлено {updated_count} сотрудников')
        ) 