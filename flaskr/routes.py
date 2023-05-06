from flask import render_template, make_response, send_file
from flaskr import app
from flaskr import definitions as constants


@app.route(constants.URL_HOME_1)
@app.route(constants.URL_HOME_2)
@app.route(constants.URL_HOME_3)
def index():
    return render_template(constants.TEMPLATE_NAME_HOME)


@app.route(constants.URL_ABOUT)
def about():
    return render_template(constants.TEMPLATE_NAME_ABOUT)


@app.route(constants.URL_BACKGROUND_IMG)
def some_resource():
    filename = constants.BACKGROUND_IMG_PATH
    response = make_response(send_file(filename))
    response.headers['Cache-Control'] = 'max-age=300' 
    return response

