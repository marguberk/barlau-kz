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
    vehicle = models.ForeignKey('logistics.Vehicle', on_delete=models.CASCADE, related_name='trips', verbose_name='Транспорт')
    driver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='trips', verbose_name='Водитель')
    start_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта отправления')
    start_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота отправления')
    end_latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Широта назначения')
    end_longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name='Долгота назначения')
    start_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес отправления')
    end_address = models.CharField(max_length=255, blank=True, verbose_name='Адрес назначения')
    cargo_description = models.TextField(verbose_name='Описание груза', blank=True)
    date = models.DateField(verbose_name='Дата поездки', default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')

    class Meta:
        verbose_name = 'Поездка'
        verbose_name_plural = 'Поездки'
        ordering = ['-date', '-created_at']

    def __str__(self):
        return f'{self.vehicle} — {self.driver} ({self.date})'

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
