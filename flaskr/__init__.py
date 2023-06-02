import logging.config
import os

from flask import Flask

app = Flask(__name__)

import flaskr.definitions as constants
from flaskr.config import DevelopmentConfig
from flaskr.web import bp_web

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

from flaskr.initialize import app_startup
app.before_first_request(app_startup)
