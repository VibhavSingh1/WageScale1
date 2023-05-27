from werkzeug.exceptions import default_exceptions
from flask import jsonify
from flaskr import app


# Register error handler for unhandled exceptions
@app.errorhandler(Exception)
def handle_exception(error):
    # Log the exception
    app.logger.exception('Unhandled Exception: %s', str(error))

    # Return a JSON error response
    response = {
        'message': 'An unexpected error occurred',
        'status_code': 500
    }
    return jsonify(response), 500


def handle_http_exception(error):
    # Log the exception
    app.logger.exception('HTTPException: %s', str(error))

    # Return a JSON error response
    response = {
        'message': error.description,
        'status_code': error.code
    }
    return jsonify(response), error.code


# Register error handlers for HTTP exceptions
for exception in default_exceptions.values():
    app.register_error_handler(exception, handle_http_exception)

