from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from model_utils import FieldTracker

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
    
    number = models.CharField(max_length=20, unique=True, verbose_name='Номер')
    brand = models.CharField(max_length=50, verbose_name='Марка')
    model = models.CharField(max_length=50, verbose_name='Модель')
    year = models.IntegerField(verbose_name='Год выпуска')
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
    driver = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'DRIVER'},
        verbose_name='Водитель'
    )
    
    def __str__(self):
        return f"{self.brand} {self.model} ({self.number})"
    
    class Meta:
        verbose_name = 'Транспортное средство'
        verbose_name_plural = 'Транспортные средства'

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
                                  related_name='assigned_tasks', verbose_name='Исполнитель')
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
        User = get_user_model()
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
