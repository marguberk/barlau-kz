from django.db.models.signals import post_save
from django.dispatch import receiver
from logistics.models import Task, WaybillDocument, Expense
from .models import Notification

@receiver(post_save, sender=Task)
def task_notification(sender, instance, created, **kwargs):
    """Создает уведомление при изменении задачи"""
    if created:
        # Уведомление для исполнителя
        if instance.assigned_to:
            Notification.create_task_notification(instance.assigned_to, instance)
        
        # Уведомление для создателя, если это разные люди
        if instance.created_by and instance.created_by != instance.assigned_to:
            Notification.create_task_notification(instance.created_by, instance)
    # Не используем проверку изменения статуса через tracker,
    # так как модель Task не имеет этого атрибута

@receiver(post_save, sender=WaybillDocument)
def waybill_notification(sender, instance, created, **kwargs):
    """Создает уведомление при создании путевого листа"""
    if created:
        # Уведомление для водителя
        Notification.create_waybill_notification(instance.driver, instance)
        
        # Уведомление для создателя, если это не водитель
        if instance.created_by != instance.driver:
            Notification.create_waybill_notification(instance.created_by, instance)

@receiver(post_save, sender=Expense)
def expense_notification(sender, instance, created, **kwargs):
    """Создает уведомление при создании расхода"""
    if created:
        # Уведомление для бухгалтера
        for accountant in instance.get_accountants():
            Notification.create_expense_notification(accountant, instance)
        
        # Уведомление для создателя, если это не бухгалтер
        if not instance.created_by.role == 'ACCOUNTANT':
            Notification.create_expense_notification(instance.created_by, instance) 