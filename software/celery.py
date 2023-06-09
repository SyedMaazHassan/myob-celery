import os
from celery import Celery
from datetime import timedelta

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'software.settings')

app = Celery('software')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# Define the beat schedule
app.conf.beat_schedule = {
    'dequeue-tasks-to-verify-teachers': {
        'task': 'datasync.celery_worker.dequeue_data_to_sync',
        'schedule': timedelta(minutes=0.5),  # Run every 1 minute
    },
}

@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
