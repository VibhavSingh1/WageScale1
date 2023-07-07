from datetime import timedelta

from celery import Celery

from flaskr import app
from flaskr import definitions as constants


# Configuring Celery
celery_app = Celery(
    app.name,
    broker=constants.CELERY_BROKER_URL,
    backend=constants.CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    result_expires=3600,
    task_track_started=True,
    imports=("flaskr.tasks",), 
    beat_schedule={
        "run_task_daily": {
            "task": "flaskr.tasks.task_flow_ConversionModuleData",
            "schedule": timedelta(
                days=1,
                # seconds=60,
            ),  # Run the task every 24 hours
            "args": (),  # Optional arguments for the task
            "options" : {
                "expires" : 3600.0,
            },
        },
    },
)
