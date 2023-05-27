import logging.config
import os
from celery import Celery
from flask import Flask

app = Flask(__name__)

from flaskr.config import DevelopmentConfig
from flaskr.web import bp_web
import flaskr.definitions as constants

blue_prints = [
    bp_web,
]
# Registering the blueprints
app.register_blueprint(bp_web)

# Configuring the Flask App
app.config.from_object(DevelopmentConfig)

# Configuring logger
if not os.path.exists(constants.LOG_TODAY_DIR):
    os.makedirs(constants.LOG_TODAY_DIR)

logging.config.dictConfig(app.config["LOGGING"])

# Configuring Celery
celery = Celery(
    app.name,
    broker=app.config['CELERY_BROKER_URL'],
    # backend=app.config['result_backend']
    backend='rpc://'  # Shunting the deprecated key
)
# celery.conf.update(app.config)

