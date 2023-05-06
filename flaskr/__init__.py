from flask import Flask
from flaskr import definitions as constants

app = Flask(__name__)

from flaskr import routes


