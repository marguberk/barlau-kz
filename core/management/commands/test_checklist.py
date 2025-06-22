from django.core.management.base import BaseCommand
from core.models import Trip, ChecklistTemplate, TripChecklist, ChecklistItem
from logistics.models import Vehicle
from accounts.models import User


class Command(BaseCommand):
    help = 'Тестирование создания поездки с чек-листом'

    def handle(self, *args, **options):
        self.stdout.write("=== Тестирование создания чек-листа ===")
        
        try:
            # Получаем первого водителя и транспорт
            driver = User.objects.filter(role='DRIVER').first()
            if not driver:
                self.stdout.write(self.style.ERROR("❌ Водитель не найден"))
                return
            
            vehicle = Vehicle.objects.filter(is_archived=False).first()
            if not vehicle:
                self.stdout.write(self.style.ERROR("❌ Транспорт не найден"))
                return
            
            self.stdout.write(f"✅ Найден водитель: {driver.get_full_name()}")
            self.stdout.write(f"✅ Найден транспорт: {vehicle.number}")
            
            # Создаем тестовую поездку
            trip = Trip.objects.create(
                title="Тестовая поездка с чек-листом",
                driver=driver,
                vehicle=vehicle,
                start_address="Алматы, Казахстан",
                end_address="Астана, Казахстан",
                cargo_description="Тестовый груз",
                start_latitude=43.238949,
                start_longitude=76.889709,
                end_latitude=51.169392,
                end_longitude=71.449074,
                status='PLANNED'
            )
            self.stdout.write(f"✅ Создана поездка: {trip.title} (ID: {trip.id})")
            
            # Проверяем количество шаблонов чек-листа
            templates_count = ChecklistTemplate.objects.filter(is_active=True).count()
            self.stdout.write(f"✅ Найдено шаблонов чек-листа: {templates_count}")
            
            if templates_count == 0:
                self.stdout.write(self.style.ERROR("❌ Шаблоны чек-листа не найдены. Запустите команду: python manage.py create_checklist_templates"))
                return
            
            # Создаем чек-лист для поездки
            checklist = TripChecklist.objects.create(
                trip=trip,
                status='PENDING'
            )
            self.stdout.write(f"✅ Создан чек-лист: ID {checklist.id}")
            
            # Создаем пункты чек-листа на основе шаблонов
            templates = ChecklistTemplate.objects.filter(is_active=True).order_by('category', 'order')
            created_items = 0
            
            for template in templates:
                ChecklistItem.objects.create(
                    checklist=checklist,
                    template=template,
                    is_checked=False,
                    is_ok=False
                )
                created_items += 1
            
            self.stdout.write(f"✅ Создано пунктов чек-листа: {created_items}")
            
            # Проверяем статистику
            total_items = checklist.items.count()
            checked_items = checklist.items.filter(is_checked=True).count()
            completion_percentage = (checked_items / total_items * 100) if total_items > 0 else 0
            
            self.stdout.write("📊 Статистика чек-листа:")
            self.stdout.write(f"   - Всего пунктов: {total_items}")
            self.stdout.write(f"   - Выполнено: {checked_items}")
            self.stdout.write(f"   - Процент выполнения: {completion_percentage:.1f}%")
            self.stdout.write(f"   - Статус: {checklist.get_status_display()}")
            
            self.stdout.write(self.style.SUCCESS("\n🎉 Тестирование завершено успешно!"))
            self.stdout.write("📝 Чек-лист доступен по адресу: http://localhost:8000/checklist/")
            self.stdout.write("🚛 Поездка доступна по адресу: http://localhost:8000/map/")
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Ошибка: {e}"))
            import traceback
            traceback.print_exc() 