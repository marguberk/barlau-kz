from django.core.management.base import BaseCommand
from core.models import ChecklistTemplate


class Command(BaseCommand):
    help = 'Создание базовых шаблонов чек-листа для проверки фуры перед рейсом'

    def handle(self, *args, **options):
        # Очищаем существующие шаблоны
        ChecklistTemplate.objects.all().delete()
        
        # Документы
        documents = [
            'Паспорт водителя',
            'Водительское удостоверение',
            'Тех паспорт авто и прицепа',
            'Таможенное свидетельство',
            'QR код очереди',
            'КАТ',
            'Китайский чип',
            'Зеленая карта',
            'Путевой лист',
            'Приглашение со склада 🇨🇳',
            'Тех осмотр',
            'Страховка на фуру и прицеп',
            'Карта допуска',
        ]
        
        for i, doc in enumerate(documents):
            ChecklistTemplate.objects.create(
                category='DOCUMENTS',
                title=doc,
                order=i + 1
            )
        
        # Внешний осмотр
        external_inspection = [
            'Целостность кузова, кабины, прицепа',
            'Отсутствие подтеков масла, топлива, охлаждающей жидкости',
            'Целостность стекол, зеркал',
            'Проверка дверей, замков и пломб',
        ]
        
        for i, item in enumerate(external_inspection):
            ChecklistTemplate.objects.create(
                category='EXTERNAL_INSPECTION',
                title=item,
                order=i + 1
            )
        
        # Состояние шин
        tires = [
            'Давление в шинах соответствует норме',
            'Протектор не изношен',
            'Нет порезов, вздутий или других повреждений',
        ]
        
        for i, item in enumerate(tires):
            ChecklistTemplate.objects.create(
                category='TIRES',
                title=item,
                order=i + 1
            )
        
        # Осветительные приборы
        lighting = [
            'Фары ближнего и дальнего света',
            'Габаритные огни',
            'Стоп-сигналы',
            'Поворотники',
            'Противотуманные фары',
            'Подсветка номера',
            'Рабочие фонари прицепа (если есть)',
        ]
        
        for i, item in enumerate(lighting):
            ChecklistTemplate.objects.create(
                category='LIGHTING',
                title=item,
                order=i + 1
            )
        
        # Электрика
        electrical = [
            'Приборная панель не показывает ошибок',
            'Аккумулятор заряжен',
            'GPS активный',
        ]
        
        for i, item in enumerate(electrical):
            ChecklistTemplate.objects.create(
                category='ELECTRICAL',
                title=item,
                order=i + 1
            )
        
        # Тормозная система
        brakes = [
            'Проверка тормозов на стоянке',
            'Проверка ручного тормоза',
            'Воздушная система без утечек',
            'Манометры в норме',
        ]
        
        for i, item in enumerate(brakes):
            ChecklistTemplate.objects.create(
                category='BRAKES',
                title=item,
                order=i + 1
            )
        
        # Жидкости
        fluids = [
            'Уровень масла в двигателе',
            'Уровень тормозной жидкости',
            'Омывающая жидкость залита',
            'Топливо в баке (расчет на весь маршрут + резерв)',
        ]
        
        for i, item in enumerate(fluids):
            ChecklistTemplate.objects.create(
                category='FLUIDS',
                title=item,
                order=i + 1
            )
        
        # Оснащение фуры
        equipment = [
            'Огнетушитель (заряжен, срок годности не истек)',
            'Аптечка (в наличии, срок годности не истек)',
            'Знак аварийной остановки',
            'Запасное колесо и домкрат',
            'Набор ключей, фонарик',
            'Жилет со светоотражающими элементами',
        ]
        
        for i, item in enumerate(equipment):
            ChecklistTemplate.objects.create(
                category='EQUIPMENT',
                title=item,
                order=i + 1
            )
        
        # Водитель
        driver = [
            'Физическое состояние водителя удовлетворительное',
            'Отдых перед рейсом соблюден',
            'Запас еды, воды, одежды',
            'Мобильная связь и навигация готовы',
        ]
        
        for i, item in enumerate(driver):
            ChecklistTemplate.objects.create(
                category='DRIVER',
                title=item,
                order=i + 1
            )
        
        total_created = ChecklistTemplate.objects.count()
        self.stdout.write(
            self.style.SUCCESS(f'Успешно создано {total_created} шаблонов чек-листа')
        ) 