from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

User = settings.AUTH_USER_MODEL

# Create your models here.

class Notification(models.Model):
    class Type(models.TextChoices):
        TASK = 'TASK', 'Задача'
        WAYBILL = 'WAYBILL', 'Путевой лист'
        EXPENSE = 'EXPENSE', 'Расход'
        SYSTEM = 'SYSTEM', 'Системное'
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_notifications')
    type = models.CharField(
        max_length=20,
        choices=Type.choices,
        verbose_name='Тип'
    )
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    message = models.TextField(verbose_name='Сообщение')
    link = models.CharField(max_length=200, verbose_name='Ссылка', blank=True)
    is_read = models.BooleanField(default=False, verbose_name='Прочитано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создано')
    
    class Meta:
        verbose_name = 'Уведомление'
        verbose_name_plural = 'Уведомления'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_type_display()}: {self.title} ({self.user})"

    @classmethod
    def create_task_notification(cls, user, task):
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
            link=reverse('task-detail', args=[task.id])
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

class Waybill(models.Model):
    number = models.CharField(max_length=50, unique=True, verbose_name='Номер КАТа')
    date = models.DateField(verbose_name='Дата', default=timezone.now)
    vehicle = models.ForeignKey('logistics.Vehicle', on_delete=models.CASCADE, related_name='core_waybills', verbose_name='Транспорт')
    driver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='core_waybills', verbose_name='Водитель')
    departure_point = models.CharField(max_length=255, verbose_name='Пункт отправления')
    destination_point = models.CharField(max_length=255, verbose_name='Пункт назначения')
    cargo_description = models.TextField(verbose_name='Описание груза', blank=True)
    cargo_weight = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Вес груза (кг)')
    created_by = models.ForeignKey(
        User, 
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

        # Создаем уведомление для водителя
        if self.driver:
            Notification.create_waybill_notification(self.driver, self)
        
        # Создаем уведомление для создателя, если это не водитель
        if self.created_by and self.created_by != self.driver:
            Notification.create_waybill_notification(self.created_by, self)

    def get_absolute_url(self):
        return reverse('core:waybill-detail', kwargs={'pk': self.pk})

def user_photo_path(instance, filename):
    # Генерируем путь для сохранения фото: photos/user_<id>/<filename>
    return f'photos/user_{instance.id}/{filename}'

class User(AbstractUser):
    class Role(models.TextChoices):
        DIRECTOR = 'DIRECTOR', _('Директор')
        ACCOUNTANT = 'ACCOUNTANT', _('Бухгалтер')
        DRIVER = 'DRIVER', _('Водитель')
        SUPPLIER = 'SUPPLIER', _('Снабженец')
        TECH = 'TECH', _('Техотдел')
        SUPERADMIN = 'SUPERADMIN', _('Суперадмин')

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.DRIVER,
        verbose_name='Роль'
    )
    phone = models.CharField(
        validators=[phone_regex],
        max_length=17,
        blank=True,
        verbose_name='Телефон'
    )
    position = models.CharField(
        max_length=100,
        blank=True,
        verbose_name='Должность'
    )
    photo = models.ImageField(
        upload_to=user_photo_path,
        null=True,
        blank=True,
        verbose_name='Фото'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
