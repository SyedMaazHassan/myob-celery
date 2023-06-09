import requests
from django.apps import apps



class BaseSyncTask:
    def __init__(self, record_id, entity, operation, delete=False):
        self.entity = entity.split('.')
        self.record_id = record_id
        self.operation = operation
        self.delete = delete
        self.app_name = self.entity[0]
        self.model_name = self.entity[1]
        self.model_class = apps.get_model(app_label=self.app_name, model_name=self.model_name)

    def sync(self):
        transformed_data = {}
        if self.operation != 'delete':
            print(self.record_id, "====")
            model_instance = self.model_class.objects.get(id=self.record_id)
            transformed_data = self.transform_data(model_instance)
        self.call_api(transformed_data, model_instance)


    def call_api(self, payload, instance):
        api_endpoint = instance.get_myob_api_endpoint(self.operation)
        if api_endpoint:
            try:
                # raise ValueError("Unsupported entity type")
                print(self.entity)
                print(api_endpoint, payload)
                instance.is_verified = True
                instance.save()
                # Doing something with the API

                # if self.operation == 'create':
                #     response = requests.post(api_endpoint, json=payload)
                # elif self.operation == 'update':
                #     response = requests.put(api_endpoint, json=payload)
                # elif self.operation == 'delete':
                #     response = requests.delete(api_endpoint, json=payload)
                # else:
                #     raise ValueError("Unsupported operation type")
                # response.raise_for_status()

                # Process the API response if needed
            except requests.exceptions.RequestException as e:
                # Handle API call error
                print(f"API call failed: {e}")
                # Perform error handling logic


class TeacherSyncTask(BaseSyncTask):
    def transform_data(self, model_instance):
        # Perform data transformation specific to ModelA
        transformed_data = {
            'recordId': model_instance.id,
            'firstName': model_instance.first_name,
            'lastName': model_instance.last_name,
            'Age': model_instance.age,
            # Map other fields as needed
        }
        return transformed_data



class StudentSyncTask(BaseSyncTask):
    def transform_data(self, model_instance):
        # Perform data transformation specific to ModelA
        transformed_data = {
            'recordId': model_instance.id,
            'firstName': model_instance.first_name,
            'lastName': model_instance.last_name,
            'Age': model_instance.age,
            # Map other fields as needed
        }
        return transformed_data





