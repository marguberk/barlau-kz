import os
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from model_utils import FieldTracker
from django.utils import timezone

User = get_user_model()

def vehicle_document_upload_path(instance, filename):
    """
    Функция для определения пути загрузки документов транспортного средства
    """
    # Получаем расширение файла
    ext = filename.split('.')[-1]
    # Формируем новое имя файла на основе id документа и транспортного средства
    if hasattr(instance, 'vehicle') and instance.vehicle:
        vehicle_id = instance.vehicle.id
    else:
        vehicle_id = 'unknown'
    # Путь для сохранения: vehicles/vehicle_id/documents/filename
    return os.path.join('vehicles', str(vehicle_id), 'documents', f"{instance.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}")

def vehicle_photo_upload_path(instance, filename):
    """
    Функция для определения пути загрузки фотографий транспортного средства
    """
    # Получаем расширение файла
    ext = filename.split('.')[-1]
    # Формируем новое имя файла
    if hasattr(instance, 'id') and instance.id:
        vehicle_id = instance.id
    else:
        vehicle_id = 'new'
    # Путь для сохранения: vehicles/vehicle_id/photos/filename
    return os.path.join('vehicles', str(vehicle_id), 'photos', f"photo_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}")

class Vehicle(models.Model):
    VEHICLE_TYPE_CHOICES = [
        ('CAR', 'Легковой'),
        ('TRUCK', 'Грузовой'),
        ('SPECIAL', 'Спецтехника'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Активен'),
        ('INACTIVE', 'Неактивен'),
        ('MAINTENANCE', 'На обслуживании'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('DIESEL', 'Дизель'),
        ('PETROL', 'Бензин'),
        ('GAS', 'Газ'),
        ('HYBRID', 'Гибрид'),
        ('ELECTRIC', 'Электро'),
    ]
    
    # Основная информация
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер')
    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год выпуска')
    color = models.CharField(max_length=50, blank=True, null=True, verbose_name='Цвет')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    vehicle_type = models.CharField(
        max_length=10, 
        choices=VEHICLE_TYPE_CHOICES, 
        default='CAR',
        verbose_name='Тип транспорта'
    )
    status = models.CharField(
        max_length=15, 
        choices=STATUS_CHOICES, 
        default='ACTIVE',
        verbose_name='Статус'
    )
    is_archived = models.BooleanField(default=False, verbose_name='В архиве')
    
    # Технические характеристики
    vin_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='VIN номер')
    engine_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер двигателя')
    chassis_number = models.CharField(max_length=30, blank=True, null=True, verbose_name='Номер шасси')
    engine_capacity = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='Объем двигателя (л)')
    fuel_type = models.CharField(max_length=20, choices=FUEL_TYPE_CHOICES, blank=True, null=True, verbose_name='Тип топлива')
    fuel_consumption = models.DecimalField(max_digits=4, decimal_places=1, blank=True, null=True, verbose_name='Расход топлива (л/100км)')
    
    # Габариты
    length = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True, verbose_name='Длина (м)')
    width = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Ширина (м)')
    height = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name='Высота (м)')
    max_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Максимальная масса (кг)')
    cargo_capacity = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True, verbose_name='Грузоподъемность (кг)')
    
    # Связи
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'DRIVER'},
        verbose_name='Водитель'
    )
    
    # Метаданные
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_vehicles',
        verbose_name='Кем создан'
    )
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"
    
    class Meta:
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'

class VehiclePhoto(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='photos', verbose_name='Транспорт')
    photo = models.ImageField(upload_to=vehicle_photo_upload_path, verbose_name='Фотография')
    description = models.CharField(max_length=100, blank=True, null=True, verbose_name='Описание')
    is_main = models.BooleanField(default=False, verbose_name='Основное фото')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name='Кем загружено')
    
    class Meta:
        verbose_name = 'Фотография транспорта'
        verbose_name_plural = 'Фотографии транспорта'
        ordering = ['-is_main', '-uploaded_at']

class VehicleDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('REGISTRATION', 'Свидетельство о регистрации'),
        ('INSURANCE', 'Страховка'),
        ('TECHNICAL_INSPECTION', 'Техосмотр'),
        ('SERVICE_BOOK', 'Сервисная книжка'),
        ('OTHER', 'Прочее'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='documents', verbose_name='Транспорт')
    document_type = models.CharField(max_length=30, choices=DOCUMENT_TYPE_CHOICES, verbose_name='Тип документа')
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер документа')
    issue_date = models.DateField(verbose_name='Дата выдачи')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    issuing_authority = models.CharField(max_length=100, blank=True, null=True, verbose_name='Кем выдан')
    description = models.TextField(blank=True, null=True, verbose_name='Примечание')
    file = models.FileField(upload_to=vehicle_document_upload_path, blank=True, null=True, verbose_name='Файл документа')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_vehicle_documents',
        verbose_name='Кем создан'
    )
    
    class Meta:
        verbose_name = 'Документ транспорта'
        verbose_name_plural = 'Документы транспорта'
        ordering = ['-issue_date']

class VehicleMaintenance(models.Model):
    MAINTENANCE_TYPE_CHOICES = [
        ('ROUTINE', 'Плановое ТО'),
        ('REPAIR', 'Ремонт'),
        ('INSPECTION', 'Осмотр'),
        ('OTHER', 'Прочее'),
    ]
    
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name='Транспорт')
    maintenance_type = models.CharField(max_length=30, choices=MAINTENANCE_TYPE_CHOICES, verbose_name='Тип обслуживания')
    date = models.DateField(verbose_name='Дата проведения')
    mileage = models.IntegerField(blank=True, null=True, verbose_name='Пробег (км)')
    description = models.TextField(verbose_name='Описание работ')
    cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Стоимость (тг)')
    next_maintenance_date = models.DateField(blank=True, null=True, verbose_name='Дата следующего ТО')
    next_maintenance_mileage = models.IntegerField(blank=True, null=True, verbose_name='Пробег для следующего ТО (км)')
    performed_by = models.CharField(max_length=100, blank=True, null=True, verbose_name='Кем проведено')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_vehicle_maintenance',
        verbose_name='Кем создано'
    )
    
    class Meta:
        verbose_name = 'Техническое обслуживание'
        verbose_name_plural = 'Техническое обслуживание'
        ordering = ['-date']

class Task(models.Model):
    PRIORITY_CHOICES = [
        ('LOW', 'Низкий'),
        ('MEDIUM', 'Средний'),
        ('HIGH', 'Высокий'),
    ]
    
    STATUS_CHOICES = [
        ('NEW', 'Новая'),
        ('IN_PROGRESS', 'В работе'),
        ('COMPLETED', 'Завершена'),
        ('CANCELLED', 'Отменена'),
    ]
    
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='MEDIUM', verbose_name='Приоритет')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='NEW', verbose_name='Статус')
    
    assigned_to = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, blank=True, 
                                  related_name='assigned_tasks', verbose_name='Основной исполнитель')
    assignees = models.ManyToManyField('accounts.User', blank=True, 
                                     related_name='task_assignments', verbose_name='Исполнители')
    vehicle = models.ForeignKey('Vehicle', on_delete=models.SET_NULL, null=True, blank=True,
                              related_name='tasks', verbose_name='Транспорт')
    
    due_date = models.DateTimeField(verbose_name='Срок выполнения')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    created_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True,
                                 related_name='created_tasks', verbose_name='Создал')
    
    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

    def get_all_assignees(self):
        """Получить всех исполнителей (основного + дополнительных)"""
        assignees = list(self.assignees.all())
        if self.assigned_to and self.assigned_to not in assignees:
            assignees.insert(0, self.assigned_to)
        return assignees

class TaskFile(models.Model):
    """Файлы и изображения прикрепленные к задаче"""
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='files', verbose_name='Задача')
    file = models.FileField(upload_to='tasks/files/%Y/%m/', verbose_name='Файл')
    original_name = models.CharField(max_length=255, verbose_name='Оригинальное имя файла')
    file_type = models.CharField(max_length=50, verbose_name='Тип файла')
    file_size = models.PositiveIntegerField(verbose_name='Размер файла (байт)')
    uploaded_by = models.ForeignKey('accounts.User', on_delete=models.SET_NULL, null=True, 
                                  related_name='uploaded_task_files', verbose_name='Загрузил')
    uploaded_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата загрузки')
    
    class Meta:
        verbose_name = 'Файл задачи'
        verbose_name_plural = 'Файлы задач'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.task.title} - {self.original_name}"
    
    @property
    def is_image(self):
        """Проверяет, является ли файл изображением"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        return any(self.original_name.lower().endswith(ext) for ext in image_extensions)
    
    def get_file_size_display(self):
        """Возвращает размер файла в человекочитаемом формате"""
        if self.file_size < 1024:
            return f"{self.file_size} Б"
        elif self.file_size < 1024 * 1024:
            return f"{self.file_size // 1024} КБ"
        else:
            return f"{self.file_size // (1024 * 1024)} МБ"

class Expense(models.Model):
    class Category(models.TextChoices):
        FUEL = 'FUEL', 'Топливо'
        MAINTENANCE = 'MAINTENANCE', 'Техобслуживание'
        REPAIR = 'REPAIR', 'Ремонт'
        OTHER = 'OTHER', 'Прочее'
    
    amount = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Сумма')
    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        verbose_name='Категория'
    )
    description = models.TextField(verbose_name='Описание')
    date = models.DateField(verbose_name='Дата')
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        verbose_name='Транспорт'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Создал'
    )
    receipt = models.ImageField(
        upload_to='receipts/',
        null=True,
        blank=True,
        verbose_name='Чек'
    )
    
    def __str__(self):
        return f"{self.get_category_display()} - {self.amount} тг"
    
    class Meta:
        verbose_name = 'Расход'
        verbose_name_plural = 'Расходы'

    def get_accountants(self):
        """Получить список бухгалтеров"""
        return User.objects.filter(role='ACCOUNTANT', is_active=True)

class WaybillDocument(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name='Номер')
    date = models.DateField(verbose_name='Дата')
    vehicle = models.ForeignKey(
        Vehicle,
        on_delete=models.CASCADE,
        verbose_name='Транспорт'
    )
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'DRIVER'},
        verbose_name='Водитель'
    )
    departure_point = models.CharField(max_length=200, verbose_name='Пункт отправления')
    destination_point = models.CharField(max_length=200, verbose_name='Пункт назначения')
    cargo_description = models.TextField(verbose_name='Описание груза')
    cargo_weight = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Вес груза (кг)'
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='created_waybills',
        verbose_name='Создал'
    )
    
    def __str__(self):
        return f"КАТ №{self.number} от {self.date}"
    
    class Meta:
        verbose_name = 'Путевой лист'
        verbose_name_plural = 'Путевые листы'