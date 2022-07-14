from __future__ import absolute_import
import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import ssl
# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_prototype.settings')
app = Celery('django_prototype',broker_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     },
     redis_backend_use_ssl = {
        'ssl_cert_reqs': ssl.CERT_NONE
     },include=['pod.task'])

# Using a string here means the worker will not have to
# pickle the object when using Windows.
app.config_from_object('django.conf:settings')
from django.apps import apps
app.autodiscover_tasks(lambda: [n.name for n in apps.get_app_configs()])

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

    
app.conf.beat_schedule = {
    # Execute the Speed Test every 10 minutes
    'network-speedtest-10min': {
        'task': 'pod.task.update_task',
        'schedule': crontab(minute='*/1'),
    },
} 