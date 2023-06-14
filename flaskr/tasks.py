# import subprocess
from flaskr.celery_conf import celery_app
from flaskr.api.services import PPPData


@celery_app.task
def work_PPP_gen():
    """Run the PPP task asynchornously
    """
    serve_api = PPPData()
    serve_api.get_ppp_data()

