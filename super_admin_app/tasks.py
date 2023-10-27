from celery import shared_task
from super_admin_app.models import GeneralNotification
from django.utils import timezone

@shared_task(bind=True)
def task_fun(self):
    for i in range(10):
        print(i)
      
    return "done"