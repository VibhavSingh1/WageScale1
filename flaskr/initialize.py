from flaskr import app
from flaskr.tasks import work_PPP_gen

def app_startup():
    """Gets executed before flask app starts serving any requests
    """
    app.logger.info("Starting the async execution of tasks")
    work_PPP_gen.apply_async()
    app.logger.info("ppp data generation task done!")


