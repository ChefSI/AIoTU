from celery import Celery
from datetime import timedelta
from django.conf import settings

app = Celery('Project')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    'get_data_every_hour': {
        'task': 'app.tasks.get_data_task',
        'schedule': timedelta(hours=1),
    },
}
