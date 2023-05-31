from flaskr import app
from flaskr import definitions as constants
from celery import Celery

# Configuring Celery
celery_app = Celery(
    app.name,
    broker=constants.CELERY_BROKER_URL,
    backend=constants.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    result_expires=3600,
    task_track_started=True,
)
