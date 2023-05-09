from flask import Flask

app = Flask(__name__)

from flaskr.config import DevelopmentConfig
from flaskr.web import bp_web

blue_prints = [
    bp_web,
]

# Configuring the Flask App
app.config.from_object(DevelopmentConfig)
# Registering the blueprints
app.register_blueprint(bp_web)
