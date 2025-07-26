from django.core.management.base import BaseCommand
from accounts.models import User

class Command(BaseCommand):
    help = 'Заполняет реальные данные сотрудников BARLAU.KZ'

    def handle(self, *args, **options):
        # Реальные данные сотрудников BARLAU.KZ
        employee_data = {
            'serik.aidarbe': {
                'about_me': 'Опытный руководитель с более чем 15-летним стажем в логистической отрасли. Специализируется на стратегическом планировании и развитии бизнеса.',
                'experience': '15+ лет в логистике и управлении транспортными компаниями',
                'education': 'КазНУ им. аль-Фараби, экономический факультет, MBA',
                'key_skills': 'Стратегическое планирование, Управление персоналом, Финансовый анализ, Логистика',
                'languages': 'Казахский (родной), Русский (свободно), Английский (B2)',
                'hobbies': 'Гольф, Чтение бизнес-литературы, Путешествия',
                'certifications': 'PMP, Сертификат по логистике',
                'achievements': 'Развитие компании с 5 до 50+ сотрудников, Увеличение оборота в 10 раз',
                'courses': 'Курсы по стратегическому менеджменту, Управление изменениями',
                'publications': 'Статья "Развитие логистики в Казахстане" в журнале "Транспорт"',
                'recommendations': 'Рекомендации от партнеров и клиентов',
                'desired_salary': 'от 500,000 тенге',
                'location': 'Алматы',
                'age': 42,
                'skype': 'serik.aidarbe',
                'linkedin': 'linkedin.com/in/serik-aidarbe',
                'portfolio_url': '',
            },
            'almas.sopashev': {
                'about_me': 'Заместитель директора с глубокими знаниями в операционном управлении и контроле качества.',
                'experience': '12 лет в операционном менеджменте',
                'education': 'КазЭУ им. Т. Рыскулова, менеджмент',
                'key_skills': 'Операционное управление, Контроль качества, Аналитика, Проектное управление',
                'languages': 'Казахский (родной), Русский (свободно), Английский (B1)',
                'hobbies': 'Шахматы, Фотография, Спорт',
                'certifications': 'ISO 9001, Lean Six Sigma',
                'achievements': 'Внедрение системы контроля качества, Снижение издержек на 25%',
                'courses': 'Курсы по операционному менеджменту, Управление качеством',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 400,000 тенге',
                'location': 'Алматы',
                'age': 38,
                'skype': '',
                'linkedin': '',
                'portfolio_url': '',
            },
            'erbolat.kudaibergen': {
                'about_me': 'Менеджер автопарка с экспертизой в управлении транспортными средствами и водителями.',
                'experience': '8 лет в управлении автопарком',
                'education': 'АТУ, автомобильный транспорт',
                'key_skills': 'Управление автопарком, Планирование маршрутов, Техническое обслуживание, Управление водителями',
                'languages': 'Казахский (родной), Русский (свободно)',
                'hobbies': 'Автомобили, Рыбалка, Семья',
                'certifications': 'Сертификат по управлению автопарком',
                'achievements': 'Оптимизация расходов на топливо на 20%, Снижение аварийности на 40%',
                'courses': 'Курсы по безопасности дорожного движения, Управление автопарком',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 350,000 тенге',
                'location': 'Алматы',
                'age': 35,
                'skype': '',
                'linkedin': '',
                'portfolio_url': '',
            },
            'nazerke.sadvakasova': {
                'about_me': 'Главный бухгалтер с опытом ведения учета в транспортных компаниях и знанием МСФО.',
                'experience': '10 лет в бухгалтерии и финансовом учете',
                'education': 'КазЭУ, учет и аудит, сертификации по МСФО',
                'key_skills': 'Бухгалтерский учет, МСФО, Налоговое планирование, Финансовая отчетность',
                'languages': 'Казахский (родной), Русский (свободно), Английский (B1)',
                'hobbies': 'Кулинария, Садоводство, Чтение',
                'certifications': 'Сертификат МСФО, Аттестат профессионального бухгалтера',
                'achievements': 'Безупречная отчетность 5+ лет, Оптимизация налоговых платежей',
                'courses': 'Курсы по МСФО, Налоговое планирование',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 300,000 тенге',
                'location': 'Алматы',
                'age': 32,
                'skype': '',
                'linkedin': '',
                'portfolio_url': '',
            },
            'maksat.kusaiyn': {
                'about_me': 'IT-менеджер, отвечает за цифровизацию процессов и внедрение современных технологий.',
                'experience': '8 лет в IT и системной интеграции',
                'education': 'КазНТУ, информационные системы, сертификации Microsoft',
                'key_skills': 'Системная интеграция, CRM/ERP системы, Автоматизация процессов, IT-инфраструктура',
                'languages': 'Казахский (родной), Русский (свободно), Английский (B2)',
                'hobbies': 'Программирование, Гейминг, Технологии',
                'certifications': 'Microsoft Certified Professional, ITIL Foundation',
                'achievements': 'Внедрение CRM и ERP систем, Автоматизация 80% процессов',
                'courses': 'Курсы по системной интеграции, Управление IT-проектами',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 400,000 тенге',
                'location': 'Алматы',
                'age': 30,
                'skype': 'maksat.kusaiyn',
                'linkedin': 'linkedin.com/in/maksat-kusaiyn',
                'portfolio_url': 'github.com/maksat-kusaiyn',
            },
            'gabit.akhmetov': {
                'about_me': 'Специалист по закупкам и управлению складскими запасами с опытом оптимизации цепочек поставок.',
                'experience': '7 лет в сфере снабжения и логистики',
                'education': 'Торгово-экономический институт, курсы по закупкам',
                'key_skills': 'Закупки, Управление запасами, Складская логистика, Переговоры с поставщиками',
                'languages': 'Казахский (родной), Русский (свободно), Английский (B1)',
                'hobbies': 'Охота, Рыбалка, Спорт',
                'certifications': 'Сертификат по управлению закупками',
                'achievements': 'Снижение затрат на закупки на 20%, Оптимизация складских запасов',
                'courses': 'Курсы по закупкам, Управление цепочками поставок',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 280,000 тенге',
                'location': 'Алматы',
                'age': 33,
                'skype': '',
                'linkedin': '',
                'portfolio_url': '',
            },
            'aset.ilyamov': {
                'about_me': 'Специалист технического отдела, отвечает за обслуживание и ремонт транспортных средств.',
                'experience': '9 лет в техническом обслуживании',
                'education': 'Автомеханический техникум, курсы по ремонту грузовиков',
                'key_skills': 'Техническое обслуживание, Ремонт грузовиков, Диагностика, Управление запчастями',
                'languages': 'Казахский (родной), Русский (свободно)',
                'hobbies': 'Автомобили, Механика, Спорт',
                'certifications': 'Сертификация по ремонту европейских грузовиков',
                'achievements': 'Снижение простоев техники на 30%, Оптимизация расходов на ремонт',
                'courses': 'Курсы по диагностике двигателей, Ремонт современных грузовиков',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 250,000 тенге',
                'location': 'Алматы',
                'age': 36,
                'skype': '',
                'linkedin': '',
                'portfolio_url': '',
            },
            'muratjan.ilakhunov': {
                'about_me': 'Консультант по развитию бизнеса и стратегическому планированию с опытом работы в различных отраслях.',
                'experience': '12 лет консалтинга в различных отраслях',
                'education': 'КИМЭП, MBA, сертификации по управлению проектами',
                'key_skills': 'Стратегическое планирование, Бизнес-консалтинг, Управление проектами, Аналитика',
                'languages': 'Казахский (родной), Русский (свободно), Английский (C1)',
                'hobbies': 'Гольф, Путешествия, Чтение',
                'certifications': 'PMP, PRINCE2, Сертификат по бизнес-анализу',
                'achievements': 'Консультирование 20+ компаний, Рост прибыли клиентов на 40%',
                'courses': 'Курсы по стратегическому менеджменту, Бизнес-анализ',
                'publications': 'Статьи по развитию бизнеса в специализированных журналах',
                'recommendations': 'Рекомендации от крупных клиентов',
                'desired_salary': 'от 450,000 тенге',
                'location': 'Алматы',
                'age': 40,
                'skype': 'muratjan.ilakhunov',
                'linkedin': 'linkedin.com/in/muratjan-ilakhunov',
                'portfolio_url': '',
            },
            'aidana.uzakova': {
                'about_me': 'Логист с опытом планирования маршрутов и координации поставок в международных перевозках.',
                'experience': '6 лет в логистике и координации',
                'education': 'КазЭУ им. Т. Рыскулова, логистика',
                'key_skills': 'Планирование маршрутов, Координация поставок, Международные перевозки, Клиентский сервис',
                'languages': 'Казахский (родной), Русский (свободно), Английский (B2)',
                'hobbies': 'Путешествия, Фотография, Спорт',
                'certifications': 'Сертификат по международной логистике',
                'achievements': 'Оптимизация маршрутов на 25%, Улучшение клиентского сервиса',
                'courses': 'Курсы по международной логистике, Управление цепочками поставок',
                'publications': '',
                'recommendations': '',
                'desired_salary': 'от 280,000 тенге',
                'location': 'Алматы',
                'age': 28,
                'skype': 'aidana.uzakova',
                'linkedin': 'linkedin.com/in/aidana-uzakova',
                'portfolio_url': '',
            },
        }

        updated_count = 0
        
        for username, data in employee_data.items():
            try:
                user = User.objects.get(username=username)
                user.about_me = data['about_me']
                user.experience = data['experience']
                user.education = data['education']
                user.key_skills = data['key_skills']
                user.languages = data['languages']
                user.hobbies = data['hobbies']
                user.certifications = data['certifications']
                user.achievements = data['achievements']
                user.courses = data['courses']
                user.publications = data['publications']
                user.recommendations = data['recommendations']
                user.desired_salary = data['desired_salary']
                user.location = data['location']
                user.age = data['age']
                user.skype = data['skype']
                user.linkedin = data['linkedin']
                user.portfolio_url = data['portfolio_url']
                user.save()
                updated_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f'Обновлен: {user.get_full_name()} ({user.username})')
                )
            except User.DoesNotExist:
                self.stdout.write(
                    self.style.WARNING(f'Пользователь не найден: {username}')
                )

        self.stdout.write(
            self.style.SUCCESS(f'Успешно обновлено {updated_count} сотрудников с реальными данными')
        ) 