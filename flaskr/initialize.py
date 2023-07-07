from flaskr import app
from flaskr.tasks import task_flow_ConversionModuleData

def app_startup():
    """Gets executed before flask app starts serving any requests
    """
    app.logger.info("Starting the async execution of tasks")
    task_flow_ConversionModuleData.apply_async()