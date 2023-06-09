from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from datasync.celery_worker import enqueue_data_to_sync


class BaseSyncModel(models.Model):
    class Meta:
        abstract = True

    @classmethod
    def get_entity_name(cls):
        return f"datasync.{cls.__name__}"

    @classmethod
    def get_entity_key(cls):
        return cls.get_entity_name()

    @classmethod
    def get_delete_entity_key(cls):
        return f"{cls.get_entity_name()}:delete"

    @classmethod
    def get_update_entity_key(cls):
        return f"{cls.get_entity_name()}:update"

    @classmethod
    def get_create_entity_key(cls):
        return f"{cls.get_entity_name()}:create"


# General signal handler for save, update
@receiver(post_save)
def enqueue_model_save(sender, instance, created, **kwargs):
    entity_name = sender.__name__
    entity_key = f"datasync.{entity_name}"
    if created:
        enqueue_data_to_sync.delay(instance.id, entity_key, 'create')
    # else:
    #     enqueue_data_to_sync.delay(instance.id, entity_key, 'update')

# General signal handler for save, delete
@receiver(post_delete)
def enqueue_model_delete(sender, instance, **kwargs):
    entity_name = sender.__name__
    entity_key = f"datasync.{entity_name}"
    enqueue_data_to_sync.delay(instance.id, entity_key, 'delete', True)


# python manage.py makemigrations
# python manage.py migrate
# python manage.py runserver


# Create your models here.
class Teacher(BaseSyncModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    is_verified = models.BooleanField(default=False)

    def get_myob_api_endpoint(self, operation):
        API_ENDPOINTS = {
            'create': 'http://api.example.com/modela/create/',
            'update': 'http://api.example.com/modela/update/',
            'delete': 'http://api.example.com/modela/delete/',
        }
        return API_ENDPOINTS[operation]


    def __str__(self):
        return self.first_name + " " + self.last_name
    


class Student(BaseSyncModel):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.IntegerField()
    is_verified = models.BooleanField(default=False)

    def get_myob_api_endpoint(self, operation):
        API_ENDPOINTS = {
            'create': 'http://api.example.com/modela/create/',
            'update': 'http://api.example.com/modela/update/',
            'delete': 'http://api.example.com/modela/delete/',
        }
        return API_ENDPOINTS[operation]

    def __str__(self):
        return self.first_name + " " + self.last_name
    

    