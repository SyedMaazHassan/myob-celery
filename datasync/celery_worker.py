from celery import shared_task
from redis import Redis
import json
from .tasks import TeacherSyncTask, StudentSyncTask


# Setup - START
redis_client = Redis(host='localhost', port=6379, db=0)

MODEL_SYNC_TASKS = {
    'datasync.Teacher': TeacherSyncTask,
    'datasync.Student': StudentSyncTask
}
# Setup - END


def get_sync_task_class(entity):
    if entity in MODEL_SYNC_TASKS:
        return MODEL_SYNC_TASKS[entity]
    else:
        raise ValueError("Unsupported entity type")
    


@shared_task
def enqueue_data_to_sync(record_id, entity, operation, delete=False):
    my_json = {
        'record_id': record_id,
        'entity': entity,
        'operation': operation,
        'delete': delete
    }
    my_json = json.dumps(my_json)
    redis_client.rpush('task_queue', my_json)



@shared_task
def dequeue_data_to_sync():
    # Logic to check for new records and enqueue tasks
    # based on the newly created records
    problematic_tasks = []
    while True:
        task = redis_client.lpop('task_queue')  # Fetch task from Redis list
        if task:
            # Task found in the queue
            task_dict = json.loads(task)
            try:
                SYNC_TASK_CLASS = get_sync_task_class(task_dict['entity'])
                task_obj = SYNC_TASK_CLASS(
                    task_dict['record_id'], 
                    task_dict['entity'], 
                    task_dict['operation'], 
                    task_dict['delete'])
                task_obj.sync()
                
            except Exception as e:
                print(f"Error occurred during task execution: {e}")
                # Re-enqueue the task for later processing
                problematic_tasks.append(task_dict)
                continue
        else:
            # No task found in the queue
            break

    # Re-enqueue the problematic tasks - in case if any api calls failed
    for task in problematic_tasks:
        enqueue_data_to_sync.delay(task['record_id'], task['entity'], task['operation'], task['delete'])
