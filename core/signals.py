from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
import logging

from .models import Notification, Trip
from logistics.models import Task, Expense, Vehicle, VehicleDocument

User = get_user_model()
logger = logging.getLogger(__name__)

class NotificationService:
    """Централизованный сервис для отправки уведомлений"""
    
    @staticmethod
    def get_recipients_by_roles(roles, exclude_user=None):
        """Получить всех пользователей с указанными ролями"""
        recipients = User.objects.filter(
            is_active=True,
            role__in=roles
        ).distinct()
        
        if exclude_user:
            recipients = recipients.exclude(id=exclude_user.id)
            
        return recipients
    
    @staticmethod
    def get_management_recipients(exclude_user=None):
        """Получить руководящий состав: директор, админ, диспетчер"""
        return NotificationService.get_recipients_by_roles(
            ['DIRECTOR', 'ADMIN', 'SUPERADMIN', 'DISPATCHER'],
            exclude_user
        )
    
    @staticmethod
    def get_financial_recipients(exclude_user=None):
        """Получить финансовых сотрудников: директор, админ, бухгалтер"""
        return NotificationService.get_recipients_by_roles(
            ['DIRECTOR', 'ADMIN', 'SUPERADMIN', 'ACCOUNTANT'],
            exclude_user
        )
    
    @staticmethod
    def send_to_multiple_users(recipients, notification_type, title, message, link='', priority=Notification.Priority.NORMAL):
        """Отправить уведомление нескольким пользователям"""
        notifications = []
        for user in recipients:
            try:
                notification = Notification.objects.create(
                    user=user,
                    type=notification_type,
                    title=title,
                    message=message,
                    link=link,
                    priority=priority
                )
                notifications.append(notification)
                logger.info(f"Уведомление отправлено пользователю {user.email}: {title}")
            except Exception as e:
                logger.error(f"Ошибка отправки уведомления пользователю {user.email}: {e}")
        
        return notifications


# СИГНАЛЫ ДЛЯ ЗАДАЧ
@receiver(post_save, sender=Task)
def task_created_updated(sender, instance, created, **kwargs):
    """Уведомления при создании или изменении задач"""
    try:
        # При создании новой задачи
        if created:
            # Уведомляем исполнителя
            if instance.assigned_to and instance.assigned_to != instance.created_by:
                Notification.create_task_notification(instance.assigned_to, instance)
            
            # Уведомляем всех исполнителей
            for assignee in instance.assignees.all():
                if assignee != instance.created_by and assignee != instance.assigned_to:
                    Notification.create_task_notification(assignee, instance)
            
            # Уведомляем руководство о новой задаче
            management = NotificationService.get_management_recipients(exclude_user=instance.created_by)
            NotificationService.send_to_multiple_users(
                recipients=management,
                notification_type=Notification.Type.TASK,
                title='Создана новая задача',
                message=f'Создана задача "{instance.title}" для {instance.assigned_to.get_full_name() if instance.assigned_to else "исполнителей"}',
                link=f'/dashboard/tasks/{instance.id}/'
            )
        
        # При изменении статуса задачи
        else:
            # Проверяем, изменился ли статус
            if hasattr(instance, '_state') and instance._state.adding is False:
                try:
                    old_instance = Task.objects.get(pk=instance.pk)
                    if hasattr(old_instance, 'status') and old_instance.status != instance.status:
                        # Статус изменился - отправляем уведомления
                        
                        # Уведомляем создателя задачи
                        if instance.created_by and instance.created_by != instance.assigned_to:
                            status_display = dict(Task.STATUS_CHOICES).get(instance.status, instance.status)
                            Notification.objects.create(
                                user=instance.created_by,
                                type=Notification.Type.TASK,
                                title='Изменен статус задачи',
                                message=f'Задача "{instance.title}" изменила статус на: {status_display}',
                                link=f'/dashboard/tasks/{instance.id}/'
                            )
                        
                        # Уведомляем руководство об изменении статуса
                        management = NotificationService.get_management_recipients()
                        status_display = dict(Task.STATUS_CHOICES).get(instance.status, instance.status)
                        NotificationService.send_to_multiple_users(
                            recipients=management,
                            notification_type=Notification.Type.TASK,
                            title='Изменен статус задачи',
                            message=f'Задача "{instance.title}" изменила статус на: {status_display}',
                            link=f'/dashboard/tasks/{instance.id}/'
                        )
                except Task.DoesNotExist:
                    pass
                    
    except Exception as e:
        logger.error(f"Ошибка в task_created_updated: {e}")


# СИГНАЛЫ ДЛЯ РАСХОДОВ
@receiver(post_save, sender=Expense)
def expense_created(sender, instance, created, **kwargs):
    """Уведомления при создании расходов"""
    if not created:
        return
        
    try:
        # Уведомляем финансовых сотрудников о новом расходе
        financial_recipients = NotificationService.get_financial_recipients(exclude_user=instance.created_by)
        
        category_display = dict(Expense.Category.choices).get(instance.category, instance.category)
        vehicle_info = f" для {instance.vehicle.brand} {instance.vehicle.model} ({instance.vehicle.number})" if instance.vehicle else ""
        
        # Определяем приоритет в зависимости от суммы
        if instance.amount > 100000:  # Большие расходы требуют внимания
            priority = Notification.Priority.HIGH
        elif instance.amount > 50000:
            priority = Notification.Priority.NORMAL
        else:
            priority = Notification.Priority.LOW
        
        NotificationService.send_to_multiple_users(
            recipients=financial_recipients,
            notification_type=Notification.Type.EXPENSE,
            title='Новый расход',
            message=f'Добавлен расход: {category_display} на сумму {instance.amount} тг{vehicle_info}',
            link=f'/dashboard/expenses/{instance.id}/',
            priority=priority
        )
        
        logger.info(f"Уведомления о расходе {instance.id} отправлены с приоритетом {priority}")
        
    except Exception as e:
        logger.error(f"Ошибка в expense_created: {e}")


# СИГНАЛЫ ДЛЯ ПОЕЗДОК
@receiver(post_save, sender=Trip)
def trip_created_updated(sender, instance, created, **kwargs):
    """Уведомления при создании или изменении поездок"""
    try:
        if created:
            # Уведомляем водителя о новой поездке
            if instance.driver:
                Notification.objects.create(
                    user=instance.driver,
                    type=Notification.Type.SYSTEM,
                    title='Новая поездка',
                    message=f'Вам назначена новая поездка: {instance.title}',
                    link=f'/dashboard/trips/{instance.id}/'
                )
            
            # Уведомляем руководство о новой поездке
            management = NotificationService.get_management_recipients()
            NotificationService.send_to_multiple_users(
                recipients=management,
                notification_type=Notification.Type.SYSTEM,
                title='Создана новая поездка',
                message=f'Создана поездка "{instance.title}" для водителя {instance.driver.get_full_name() if instance.driver else "неизвестно"}',
                link=f'/dashboard/trips/{instance.id}/'
            )
        
        else:
            # Проверяем изменение статуса поездки
            if hasattr(instance, '_state') and instance._state.adding is False:
                try:
                    old_instance = Trip.objects.get(pk=instance.pk)
                    if hasattr(old_instance, 'status') and old_instance.status != instance.status:
                        # Статус поездки изменился
                        
                        status_display = dict(Trip.STATUS_CHOICES).get(instance.status, instance.status)
                        
                        # Уведомляем водителя об изменении статуса
                        if instance.driver:
                            Notification.objects.create(
                                user=instance.driver,
                                type=Notification.Type.SYSTEM,
                                title='Изменен статус поездки',
                                message=f'Поездка "{instance.title}" изменила статус на: {status_display}',
                                link=f'/dashboard/trips/{instance.id}/'
                            )
                        
                        # Уведомляем руководство об изменении статуса
                        management = NotificationService.get_management_recipients()
                        NotificationService.send_to_multiple_users(
                            recipients=management,
                            notification_type=Notification.Type.SYSTEM,
                            title='Изменен статус поездки',
                            message=f'Поездка "{instance.title}" изменила статус на: {status_display}',
                            link=f'/dashboard/trips/{instance.id}/'
                        )
                        
                except Trip.DoesNotExist:
                    pass
                    
    except Exception as e:
        logger.error(f"Ошибка в trip_created_updated: {e}")


# СИГНАЛЫ ДЛЯ ТРАНСПОРТА
@receiver(post_save, sender=Vehicle)
def vehicle_created(sender, instance, created, **kwargs):
    """Уведомления при добавлении нового транспорта"""
    if not created:
        return
        
    try:
        # Уведомляем руководство о новом транспорте
        management = NotificationService.get_management_recipients()
        NotificationService.send_to_multiple_users(
            recipients=management,
            notification_type=Notification.Type.SYSTEM,
            title='Добавлен новый транспорт',
            message=f'В систему добавлен транспорт: {instance.brand} {instance.model} ({instance.number})',
            link=f'/dashboard/vehicles/{instance.id}/'
        )
        
        logger.info(f"Уведомления о новом транспорте {instance.id} отправлены")
        
    except Exception as e:
        logger.error(f"Ошибка в vehicle_created: {e}")


# СИГНАЛЫ ДЛЯ ДОКУМЕНТОВ ТРАНСПОРТА
@receiver(post_save, sender=VehicleDocument)
def vehicle_document_saved(sender, instance, created, **kwargs):
    """Проверка сроков действия документов при сохранении"""
    if not instance.expiry_date:
        return
        
    try:
        today = timezone.now().date()
        days_left = (instance.expiry_date - today).days
        
        # Уведомляем за 30, 14, 7 и 1 день до истечения
        if days_left in [30, 14, 7, 1] or (0 <= days_left <= 3):
            recipients = NotificationService.get_management_recipients()
            
            doc_type_display = dict(VehicleDocument.DOCUMENT_TYPE_CHOICES).get(
                instance.document_type, 
                instance.document_type
            )
            
            if days_left <= 0:
                title = 'Истек срок действия документа!'
                message = f'СРОЧНО! У {instance.vehicle.brand} {instance.vehicle.model} ({instance.vehicle.number}) истек срок: {doc_type_display}'
            elif days_left == 1:
                title = 'Завтра истекает срок документа!'
                message = f'ВНИМАНИЕ! У {instance.vehicle.brand} {instance.vehicle.model} ({instance.vehicle.number}) завтра истекает: {doc_type_display}'
            else:
                title = 'Скоро истекает срок документа'
                message = f'У {instance.vehicle.brand} {instance.vehicle.model} ({instance.vehicle.number}) через {days_left} дн. истекает: {doc_type_display}'
            
            # Проверяем, не отправляли ли уже уведомление за этот период
            existing_notifications = Notification.objects.filter(
                type=Notification.Type.DOCUMENT,
                message__contains=instance.expiry_date.strftime('%d.%m.%Y'),
                created_at__gte=today - timedelta(days=1)
            )
            
            if not existing_notifications.exists():
                NotificationService.send_to_multiple_users(
                    recipients=recipients,
                    notification_type=Notification.Type.DOCUMENT,
                    title=title,
                    message=f'{message} — {instance.expiry_date.strftime("%d.%m.%Y")}',
                    link=f'/dashboard/vehicles/{instance.vehicle.id}/'
                )
                
                logger.info(f"Уведомления об истечении документа {instance.id} отправлены")
    
    except Exception as e:
        logger.error(f"Ошибка в vehicle_document_saved: {e}")


# ФУНКЦИЯ ДЛЯ РЕГУЛЯРНОЙ ПРОВЕРКИ СРОКОВ ДОКУМЕНТОВ
def check_expiring_documents():
    """Регулярная проверка истечения сроков документов (можно вызывать из cron)"""
    try:
        today = timezone.now().date()
        
        # Находим документы, которые истекают в ближайшие 30 дней
        expiring_docs = VehicleDocument.objects.filter(
            expiry_date__isnull=False,
            expiry_date__lte=today + timedelta(days=30),
            expiry_date__gte=today - timedelta(days=3)  # Включаем просроченные до 3 дней
        )
        
        for doc in expiring_docs:
            days_left = (doc.expiry_date - today).days
            
            # Отправляем уведомления за определенные промежутки
            if days_left in [30, 14, 7, 3, 1] or days_left <= 0:
                recipients = NotificationService.get_management_recipients()
                
                doc_type_display = dict(VehicleDocument.DOCUMENT_TYPE_CHOICES).get(
                    doc.document_type, 
                    doc.document_type
                )
                
                if days_left <= 0:
                    title = 'Истек срок действия документа!'
                    urgency = 'СРОЧНО!'
                elif days_left <= 3:
                    title = 'Критически мало времени!'
                    urgency = 'ВНИМАНИЕ!'
                elif days_left <= 7:
                    title = 'Скоро истекает срок документа'
                    urgency = 'ВНИМАНИЕ!'
                else:
                    title = 'Скоро истекает срок документа'
                    urgency = ''
                
                message = f'{urgency} У {doc.vehicle.brand} {doc.vehicle.model} ({doc.vehicle.number}) '
                if days_left <= 0:
                    message += f'истек срок: {doc_type_display}'
                elif days_left == 1:
                    message += f'завтра истекает: {doc_type_display}'
                else:
                    message += f'через {days_left} дн. истекает: {doc_type_display}'
                
                # Проверяем, не отправляли ли уже уведомление сегодня
                existing_notifications = Notification.objects.filter(
                    type=Notification.Type.DOCUMENT,
                    message__contains=doc.expiry_date.strftime('%d.%m.%Y'),
                    created_at__date=today
                )
                
                if not existing_notifications.exists():
                    NotificationService.send_to_multiple_users(
                        recipients=recipients,
                        notification_type=Notification.Type.DOCUMENT,
                        title=title,
                        message=f'{message} — {doc.expiry_date.strftime("%d.%m.%Y")}',
                        link=f'/dashboard/vehicles/{doc.vehicle.id}/'
                    )
        
        logger.info(f"Проверка истечения документов завершена. Проверено документов: {expiring_docs.count()}")
        
    except Exception as e:
        logger.error(f"Ошибка при проверке истечения документов: {e}") 