import os
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField

def user_photo_path(instance, filename):
    # Генерируем путь для сохранения фото: photos/user_<id>/<filename>
    return f'photos/user_{instance.id}/{filename}'

def user_recommendation_path(instance, filename):
    # Генерируем путь для сохранения файла рекомендации: recommendations/user_<id>/<filename>
    return f'recommendations/user_{instance.id}/{filename}'

def driver_document_upload_path(instance, filename):
    """
    Функция для определения пути загрузки документов водителя
    """
    # Получаем расширение файла
    ext = filename.split('.')[-1]
    # Формируем новое имя файла на основе id документа и водителя
    if hasattr(instance, 'driver') and instance.driver:
        driver_id = instance.driver.id
    else:
        driver_id = 'unknown'
    # Путь для сохранения: drivers/driver_id/documents/filename
    return os.path.join('drivers', str(driver_id), 'documents', f"{instance.id}_{timezone.now().strftime('%Y%m%d%H%M%S')}.{ext}")

class User(AbstractUser):
    class Role(models.TextChoices):
        DIRECTOR = 'DIRECTOR', _('Директор')
        ACCOUNTANT = 'ACCOUNTANT', _('Бухгалтер')
        DRIVER = 'DRIVER', _('Водитель')
        SUPPLIER = 'SUPPLIER', _('Снабженец')
        TECH = 'TECH', _('Техотдел')
        MANAGER = 'MANAGER', _('Менеджер')
        DISPATCHER = 'DISPATCHER', _('Диспетчер')
        LOGIST = 'LOGIST', _('Логист')
        CONSULTANT = 'CONSULTANT', _('Консультант')
        IT_MANAGER = 'IT_MANAGER', _('IT-менеджер')
        DEPUTY_DIRECTOR = 'DEPUTY_DIRECTOR', _('Зам. директора')
        SUPERADMIN = 'SUPERADMIN', _('Суперадмин')
        EMPLOYEE = 'EMPLOYEE', _('Сотрудник')

    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{9,15}$',
        message="Номер телефона должен быть в формате: '+999999999'. До 15 цифр."
    )

    email = models.EmailField(_('email address'), unique=True)
    phone = models.CharField(_('phone number'), max_length=20, blank=True)
    role = models.CharField(_('role'), max_length=20, choices=Role.choices, default=Role.DRIVER)
    position = models.CharField(_('position'), max_length=100, blank=True)
    photo = models.ImageField(_('photo'), upload_to='employee_photos/', blank=True, null=True)
    
    # Расширенные поля для резюме
    experience = models.TextField(_('work experience'), blank=True)
    education = models.TextField(_('education'), blank=True)
    skills = models.TextField(_('skills'), blank=True)
    certifications = models.TextField(_('certifications'), blank=True)
    languages = models.TextField(_('languages'), blank=True)
    
    # Дополнительные поля для расширенного резюме
    desired_salary = models.CharField(_('desired salary'), max_length=50, blank=True)
    age = models.PositiveIntegerField(_('age'), null=True, blank=True)
    location = models.CharField(_('location'), max_length=100, blank=True)
    skype = models.CharField(_('skype'), max_length=50, blank=True)
    linkedin = models.URLField(_('linkedin'), max_length=200, blank=True)
    portfolio_url = models.URLField(_('portfolio url'), max_length=200, blank=True)
    about_me = models.TextField(_('about me'), blank=True)
    key_skills = models.TextField(_('key skills'), blank=True)
    achievements = models.TextField(_('achievements'), blank=True)
    courses = models.TextField(_('courses'), blank=True)
    publications = models.TextField(_('publications'), blank=True)
    recommendations = models.TextField(_('recommendations'), blank=True)
    hobbies = models.TextField(_('hobbies'), blank=True)
    recommendation_file = models.FileField(_('recommendation file'), upload_to=user_recommendation_path, blank=True, null=True)

    # Переопределяем поля из AbstractUser для добавления related_name
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='custom_user_set',
        related_query_name='custom_user'
    )

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} ({self.get_role_display()})"

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    # Дополнительные поля для водителей
    current_latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    current_longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    # Дополнительные поля для резюме
    is_phone_verified = models.BooleanField(default=False)
    firebase_uid = models.CharField(max_length=128, unique=True, null=True, blank=True)
    is_archived = models.BooleanField(_('archived'), default=False, help_text=_('Designates whether this user is archived and no longer active.'))


class DriverDocument(models.Model):
    DOCUMENT_TYPE_CHOICES = [
        ('DRIVER_LICENSE', 'Водительское удостоверение'),
        ('MEDICAL_CERTIFICATE', 'Медицинская справка'),
        ('PASSPORT', 'Паспорт'),
        ('WORK_PERMIT', 'Разрешение на работу'),
        ('INSURANCE', 'Страховка'),
        ('OTHER', 'Прочее'),
    ]
    
    driver = models.ForeignKey(
        'User', 
        on_delete=models.CASCADE, 
        related_name='documents', 
        limit_choices_to={'role': 'DRIVER'},
        verbose_name='Водитель'
    )
    document_type = models.CharField(
        max_length=30, 
        choices=DOCUMENT_TYPE_CHOICES, 
        verbose_name='Тип документа'
    )
    number = models.CharField(max_length=50, blank=True, null=True, verbose_name='Номер документа')
    issue_date = models.DateField(verbose_name='Дата выдачи')
    expiry_date = models.DateField(blank=True, null=True, verbose_name='Дата окончания')
    issuing_authority = models.CharField(max_length=100, blank=True, null=True, verbose_name='Кем выдан')
    description = models.TextField(blank=True, null=True, verbose_name='Примечание')
    file = models.FileField(
        upload_to=driver_document_upload_path, 
        blank=True, 
        null=True, 
        verbose_name='Файл документа'
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    created_by = models.ForeignKey(
        'User',
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_driver_documents',
        verbose_name='Кем создан'
    )
    
    class Meta:
        verbose_name = 'Документ водителя'
        verbose_name_plural = 'Документы водителей'
        ordering = ['-issue_date']
    
    def __str__(self):
        return f"{self.driver.get_full_name()} - {self.get_document_type_display()}"
