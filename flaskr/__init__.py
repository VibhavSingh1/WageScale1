import logging.config
import os

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



