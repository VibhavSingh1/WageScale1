import os
from flaskr import app
from flask import render_template, Blueprint, make_response, send_file
from flaskr.api.services import CurrencyData, ExchangeRateData
import flaskr.errorhandler



bp_web = Blueprint(
    "web_routes",
    __name__,
    static_folder="static",
    template_folder="templates",
)

# It's a good practice to explicitly add these:
# Add the static folder to the blueprint
bp_web.static_folder = "static"
# Add the templates folder to the blueprint
bp_web.template_folder = "templates"

@bp_web.route("/")
@bp_web.route("/index")
@bp_web.route("/home")
def index():
    return render_template("index.html", index=True)


@bp_web.route("/about")
def about():
    CurrencyData().get_currency_data()
    ExchangeRateData().get_exch_rate_data()
    return render_template("about.html", about=True)

@bp_web.route("/static/images/<path:filename>")
def some_resource(filename):
    filename = os.path.join(bp_web.static_folder, "images", filename)
    response = make_response(send_file(filename))
    response.headers["Cache-Control"] = "max-age=300"
    return response



