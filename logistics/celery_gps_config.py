from celery import Celery
from celery.schedules import crontab

# Создаем экземпляр Celery
app = Celery('barlau')

# Конфигурация Celery
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматическое обнаружение задач
app.autodiscover_tasks()

# Периодические задачи
app.conf.beat_schedule = {
    'sync-gps-data-every-5-seconds': {
        'task': 'logistics.tasks_gps.sync_gps_data_periodic',
        'schedule': 5.0,  # Каждые 5 секунд
    },
    'sync-gps-data-every-minute': {
        'task': 'logistics.tasks_gps.sync_gps_data_periodic',
        'schedule': crontab(minute='*'),  # Каждую минуту
    },
}

app.conf.timezone = 'Asia/Almaty'
