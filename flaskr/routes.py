import os
from flask import render_template, make_response, send_file
from flaskr import app
from flaskr import definitions as constants


@app.route(constants.URL_HOME_1) # /
@app.route(constants.URL_HOME_2) # /index
@app.route(constants.URL_HOME_3) # /home
def index():
    return render_template(constants.TEMPLATE_NAME_HOME)


@app.route(constants.URL_ABOUT) # /about
def about():
    return render_template(constants.TEMPLATE_NAME_ABOUT)


@app.route("/static/images/<filename>")
def some_resource(filename):
    filename = os.path.join(
        constants.STATIC_DIR_NAME,
        constants.IMAGES_DIR_NAME,
        filename,
        )
    response = make_response(send_file(filename))
    response.headers['Cache-Control'] = 'max-age=300' 
    return response

