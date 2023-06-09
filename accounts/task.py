from celery import shared_task
from time import sleep
from django.core.mail import send_mail

@shared_task
def sleepy(duration):
    sleep(duration)
    return None


@shared_task
def send_email_task_with_celery():
    send_mail(
        'Celery Task Worked!',
        'This is proof the task worked!',
        'hafizmaazhassan33@gmail.com',
        ['syedmaazhussain33@gmail.com'],
        fail_silently=False
    )
    return None
