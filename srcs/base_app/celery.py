import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "srcs.base_app.settings")

app = Celery("base_app")
app.conf.broker_connection_retry_on_startup = True

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
