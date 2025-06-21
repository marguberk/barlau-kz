from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    class Type(models.TextChoices):
        TASK = 'TASK', 'Задача'
        WAYBILL = 'WAYBILL', 'Путевой лист'
        EXPENSE = 'EXPENSE', 'Расход'
        SYSTEM = 'SYSTEM', 'Системное'
        DOCUMENT = 'DOCUMENT', 'Документ'
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='core_notifications')
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name='Тип'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    link = models.CharField(max_length=255, verbose_name='Ссылка', blank=True, null=True)
    read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.title} ({self.user})"

    @classmethod
    def create_task_notification(cls, user, task):
        print(f"[DEBUG] Notification.create_task_notification: user={user}, task={task}")
        """Создать уведомление о задаче"""
        if task.status == 'NEW':
            title = 'Новая задача'
            message = f'Вам назначена новая задача: {task.title}'
        elif task.status == 'IN_PROGRESS':
            title = 'Задача в работе'
            message = f'Задача "{task.title}" взята в работу'
        elif task.status == 'COMPLETED':
            title = 'Задача выполнена'
            message = f'Задача "{task.title}" выполнена'
        else:
            title = 'Задача отменена'
            message = f'Задача "{task.title}" отменена'

        return cls.objects.create(
            user=user,
            type=cls.Type.TASK,
            title=title,
            message=message,
            link=reverse('core:tasks')
        )

    @classmethod
    def create_waybill_notification(cls, user, waybill):
        """Создать уведомление о путевом листе"""
        cls.objects.create(
            user=user,
            type=cls.Type.WAYBILL,
            title="Новый путевой лист",
            message=f"Создан новый путевой лист №{waybill.number}"
        )

    @classmethod
    def create_expense_notification(cls, user, expense):
        """Создать уведомление о расходе"""
        return cls.objects.create(
            user=user,
            type=cls.Type.EXPENSE,
            title='Новый расход',
            message=f'Добавлен новый расход на сумму {expense.amount} тг',
            link=reverse('expense-detail', args=[expense.id])
        )

    @classmethod
    def create_system_notification(cls, user, title, message, link=''):
        """Создать системное уведомление"""
        return cls.objects.create(
            user=user,
            type=cls.Type.SYSTEM,
            title=title,
            message=message,
            link=link
        )

    @classmethod
    def create_vehicle_notification(cls, user, vehicle):
        print(f"[DEBUG] Notification.create_vehicle_notification: user={user}, vehicle={vehicle}")
        """Создать уведомление о новом транспорте"""
        return cls.objects.create(
            user=user,
            type=cls.Type.SYSTEM,
            title='Добавлен новый транспорт',
            message=f'Транспорт {vehicle.brand} {vehicle.model} ({vehicle.number}) успешно добавлен',
            link=f'/trucks/{vehicle.id}/'
        )

class Waybill(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name='Номер КАТа')
    date = models.DateField(verbose_name='Дата', default=timezone.now)
    vehicle = models.ForeignKey('logistics.Vehicle', on_delete=models.CASCADE, related_name='core_waybills', verbose_name='Транспорт')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='core_waybills', verbose_name='Водитель')
    departure_point = models.CharField(max_length=255, verbose_name='Пункт отправления')
    destination_point = models.CharField(max_length=255, verbose_name='Пункт назначения')
    cargo_description = models.TextField(verbose_name='Описание груза', blank=True)
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес груза (кг)')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='core_created_waybills',
        verbose_name='Создал'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Путевой лист'
        verbose_name_plural = 'Путевые листы'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'КАТ №{self.number} от {self.date}'

    def save(self, *args, **kwargs):
        if not self.number:
            # Генерируем номер в формате КАТ-ГГММДД-XXX
            date_str = timezone.now().strftime('%y%m%d')
            last_waybill = Waybill.objects.filter(
                number__startswith=f'КАТ-{date_str}'
            ).order_by('-number').first()
            
            if last_waybill:
                last_number = int(last_waybill.number.split('-')[-1])
                new_number = str(last_number + 1).zfill(3)
            else:
                new_number = '001'
                
            self.number = f'КАТ-{date_str}-{new_number}'
        
        super().save(*args, **kwargs)
        # ... уведомления больше не создаём здесь, теперь только в API

    def get_absolute_url(self):
        return reverse('core:waybill-detail', kwargs={'pk': self.pk})

class Trip(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Запланирована'),
        ('PENDING_CHECKLIST', 'Ожидает чек-лист'),
        ('READY', 'Готова к отправке'),
        ('ACTIVE', 'В пути'),
        ('COMPLETED', 'Завершена'),
        ('CANCELLED', 'Отменена'),
    ]
    
    FREIGHT_PAYMENT_CHOICES = [
        ('CASH', 'Наличные'),
        ('TRANSFER', 'Перечисление'),
    ]
    
    CARGO_TYPE_CHOICES = [
        ('CUSTOMS', 'Растаможка'),
        ('DIRECT', 'Прямой склад'),
        ('OTHER', 'Прочее'),
    ]
    
    # Основная информация
    title = models.CharField(max_length=200, verbose_name='Название поездки', default='Поездка')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PLANNED', verbose_name='Статус')
    requires_checklist = models.BooleanField(default=True, verbose_name='Требует чек-лист')
    
    # Транспорт и водитель
    vehicle = models.ForeignKey('logistics.Vehicle', on_delete=models.CASCADE, related_name='trips', verbose_name='Фура')
    trailer = models.ForeignKey('logistics.Vehicle', on_delete=models.SET_NULL, null=True, blank=True, related_name='trailer_trips', verbose_name='Прицеп')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips', verbose_name='Водитель')
    
    # Маршрут
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта отправления')
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота отправления')
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта назначения')
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота назначения')
    start_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес отправления')
    end_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес назначения')
    
    # Информация о грузе
    cargo_description = models.TextField(verbose_name='Описание груза', blank=True)
    cargo_type = models.CharField(max_length=20, choices=CARGO_TYPE_CHOICES, default='OTHER', verbose_name='Тип груза')
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name='Вес груза (кг)')
    
    # Фрахт
    freight_amount = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name='Сумма фрахта (тг)')
    freight_payment_type = models.CharField(max_length=20, choices=FREIGHT_PAYMENT_CHOICES, default='TRANSFER', verbose_name='Тип оплаты фрахта')
    
    # Даты
    planned_start_date = models.DateTimeField(default=timezone.now, verbose_name='Планируемая дата начала')
    planned_end_date = models.DateTimeField(null=True, blank=True, verbose_name='Планируемая дата окончания')
    actual_start_date = models.DateTimeField(null=True, blank=True, verbose_name='Фактическая дата начала')
    actual_end_date = models.DateTimeField(null=True, blank=True, verbose_name='Фактическая дата окончания')
    
    # Дополнительная информация
    notes = models.TextField(blank=True, verbose_name='Примечания и дополнительная информация')
    
    # Метаданные
    date = models.DateField(verbose_name='Дата поездки', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлено')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='created_trips',
        verbose_name='Создал'
    )

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
        ordering = ['-planned_start_date', '-created_at']

    def __str__(self):
        return f'{self.title} — {self.vehicle} ({self.get_status_display()})'
    
    @property
    def current_location(self):
        """Получить текущую локацию водителя"""
        if hasattr(self.driver, 'current_latitude') and hasattr(self.driver, 'current_longitude'):
            if self.driver.current_latitude and self.driver.current_longitude:
                return {
                    'latitude': float(self.driver.current_latitude),
                    'longitude': float(self.driver.current_longitude),
                    'last_update': self.driver.last_location_update
                }
        return None
    
    @property
    def route_info(self):
        """Получить информацию о маршруте"""
        return {
            'start': {
                'address': self.start_address,
                'latitude': float(self.start_latitude),
                'longitude': float(self.start_longitude)
            },
            'end': {
                'address': self.end_address,
                'latitude': float(self.end_latitude),
                'longitude': float(self.end_longitude)
            }
        }
    
    @property
    def vehicle_info(self):
        """Получить информацию о транспорте"""
        info = {
            'main': {
                'number': self.vehicle.number,
                'brand': self.vehicle.brand,
                'model': self.vehicle.model,
                'type': self.vehicle.get_vehicle_type_display()
            }
        }
        if self.trailer:
            info['trailer'] = {
                'number': self.trailer.number,
                'brand': self.trailer.brand,
                'model': self.trailer.model,
                'type': self.trailer.get_vehicle_type_display()
            }
        return info

class DriverLocation(models.Model):
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='locations', verbose_name='Водитель')
    latitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name='Широта')
    longitude = models.DecimalField(max_digits=18, decimal_places=15, verbose_name='Долгота')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='Время')
    trip = models.ForeignKey(Trip, on_delete=models.SET_NULL, null=True, blank=True, related_name='locations', verbose_name='Поездка')

    class Meta:
        verbose_name = 'Геолокация водителя'
        verbose_name_plural = 'Геолокации водителей'
        ordering = ['-timestamp']

    def __str__(self):
        return f'{self.driver} ({self.latitude}, {self.longitude}) @ {self.timestamp}'


class ChecklistTemplate(models.Model):
    """Шаблон чек-листа с предустановленными пунктами проверки"""
    
    CATEGORY_CHOICES = [
        ('DOCUMENTS', 'Документы'),
        ('EXTERNAL_INSPECTION', 'Внешний осмотр'),
        ('TIRES', 'Состояние шин'),
        ('LIGHTING', 'Осветительные приборы'),
        ('ELECTRICAL', 'Электрика'),
        ('BRAKES', 'Тормозная система'),
        ('FLUIDS', 'Жидкости'),
        ('EQUIPMENT', 'Оснащение фуры'),
        ('DRIVER', 'Водитель'),
    ]
    
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, verbose_name='Категория')
    title = models.CharField(max_length=200, verbose_name='Название пункта')
    description = models.TextField(blank=True, verbose_name='Описание')
    is_required = models.BooleanField(default=True, verbose_name='Обязательный пункт')
    order = models.IntegerField(default=0, verbose_name='Порядок')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    
    class Meta:
        verbose_name = 'Шаблон чек-листа'
        verbose_name_plural = 'Шаблоны чек-листа'
        ordering = ['category', 'order', 'title']
    
    def __str__(self):
        return f'{self.get_category_display()}: {self.title}'


class TripChecklist(models.Model):
    """Чек-лист для конкретной поездки"""
    
    STATUS_CHOICES = [
        ('PENDING', 'Ожидает проверки'),
        ('IN_PROGRESS', 'В процессе'),
        ('COMPLETED', 'Завершен'),
        ('APPROVED', 'Утвержден'),
    ]
    
    trip = models.OneToOneField(Trip, on_delete=models.CASCADE, related_name='checklist', verbose_name='Поездка')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING', verbose_name='Статус')
    
    # Подписи ответственных лиц
    driver_signature = models.CharField(max_length=100, blank=True, verbose_name='Подпись водителя')
    driver_signed_at = models.DateTimeField(null=True, blank=True, verbose_name='Время подписи водителя')
    
    mechanic_signature = models.CharField(max_length=100, blank=True, verbose_name='Подпись механика')
    mechanic_signed_at = models.DateTimeField(null=True, blank=True, verbose_name='Время подписи механика')
    mechanic = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='mechanic_checklists',
        verbose_name='Механик'
    )
    
    deputy_director_signature = models.CharField(max_length=100, blank=True, verbose_name='Подпись зам директора')
    deputy_director_signed_at = models.DateTimeField(null=True, blank=True, verbose_name='Время подписи зам директора')
    deputy_director = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='deputy_director_checklists',
        verbose_name='Зам директор'
    )
    
    # Общие поля
    notes = models.TextField(blank=True, verbose_name='Примечания')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Обновлен')
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name='Завершен')
    
    class Meta:
        verbose_name = 'Чек-лист поездки'
        verbose_name_plural = 'Чек-листы поездок'
        ordering = ['-created_at']
    
    def __str__(self):
        return f'Чек-лист для поездки {self.trip.title}'
    
    @property
    def is_fully_signed(self):
        """Проверка, что все необходимые подписи получены"""
        return all([
            self.driver_signature,
            self.mechanic_signature,
            self.deputy_director_signature
        ])
    
    @property
    def completion_percentage(self):
        """Процент выполнения чек-листа"""
        total_items = self.items.count()
        if total_items == 0:
            return 0
        completed_items = self.items.filter(is_checked=True).count()
        return round((completed_items / total_items) * 100)
    
    def save(self, *args, **kwargs):
        """Автоматическое обновление статуса поездки при изменении чек-листа"""
        super().save(*args, **kwargs)
        
        # Обновляем статус поездки в зависимости от статуса чек-листа
        if self.status == 'APPROVED':
            # Если чек-лист одобрен, поездка готова к отправке
            if self.trip.status in ['PLANNED', 'PENDING_CHECKLIST']:
                self.trip.status = 'READY'
                self.trip.save(update_fields=['status'])
        elif self.status == 'COMPLETED':
            # Если чек-лист заполнен, но не одобрен, поездка ожидает чек-лист
            if self.trip.status == 'PLANNED':
                self.trip.status = 'PENDING_CHECKLIST'
                self.trip.save(update_fields=['status'])
        elif self.status in ['PENDING', 'IN_PROGRESS']:
            # Если чек-лист в процессе или ожидает, поездка тоже ожидает
            if self.trip.status in ['READY']:
                self.trip.status = 'PENDING_CHECKLIST'
                self.trip.save(update_fields=['status'])


class ChecklistItem(models.Model):
    """Пункт чек-листа для конкретной поездки"""
    
    checklist = models.ForeignKey(TripChecklist, on_delete=models.CASCADE, related_name='items', verbose_name='Чек-лист')
    template = models.ForeignKey(ChecklistTemplate, on_delete=models.CASCADE, null=True, blank=True, verbose_name='Шаблон пункта')
    
    is_checked = models.BooleanField(default=False, verbose_name='Проверено')
    is_ok = models.BooleanField(default=True, verbose_name='В порядке')
    notes = models.TextField(blank=True, verbose_name='Примечания')
    
    checked_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        verbose_name='Проверил'
    )
    checked_at = models.DateTimeField(null=True, blank=True, verbose_name='Время проверки')
    
    # Для прикрепления фото проблем
    photo = models.ImageField(upload_to='checklist_photos/%Y/%m/', blank=True, null=True, verbose_name='Фото')
    
    class Meta:
        verbose_name = 'Пункт чек-листа'
        verbose_name_plural = 'Пункты чек-листа'
        ordering = ['template__category', 'template__order']
        unique_together = ['checklist', 'template']
    
    def __str__(self):
        status = "✓" if self.is_checked else "○"
        return f'{status} {self.template.title}'
    
    def save(self, *args, **kwargs):
        if self.is_checked and not self.checked_at:
            self.checked_at = timezone.now()
        super().save(*args, **kwargs)
        
        # Автоматически обновляем статус чек-листа
        self.update_checklist_status()
    
    def update_checklist_status(self):
        """Обновление статуса чек-листа на основе заполненности пунктов"""
        checklist = self.checklist
        
        # Проверяем процент выполнения
        completion_percentage = checklist.completion_percentage
        
        if completion_percentage == 100:
            # Если все пункты заполнены, переводим в статус "Завершен"
            if checklist.status != 'COMPLETED':
                checklist.status = 'COMPLETED'
                checklist.completed_at = timezone.now()
                checklist.save()
        elif completion_percentage > 0:
            # Если есть заполненные пункты, переводим в статус "В процессе"
            if checklist.status == 'PENDING':
                checklist.status = 'IN_PROGRESS'
                checklist.save()
        else:
            # Если ни один пункт не заполнен, оставляем в статусе "Ожидает"
            if checklist.status not in ['PENDING', 'APPROVED']:
                checklist.status = 'PENDING'
                checklist.save()


class ChecklistItemPhoto(models.Model):
    """Фото для пунктов чек-листа"""
    
    item = models.ForeignKey(ChecklistItem, on_delete=models.CASCADE, related_name='photos', verbose_name='Пункт чек-листа')
    image = models.ImageField(upload_to='checklist_photos/%Y/%m/', verbose_name='Фото')
    description = models.CharField(max_length=255, blank=True, verbose_name='Описание')
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        verbose_name='Загрузил'
    )
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Время загрузки')
    
    class Meta:
        verbose_name = 'Фото пункта чек-листа'
        verbose_name_plural = 'Фото пунктов чек-листа'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f'Фото для {self.item} - {self.uploaded_at}'
