# import subprocess
from flaskr.celery_conf import celery_app
from flaskr.api.services import Serve3rdPartyAPI


@celery_app.task
def work_PPP_gen():
    """Run the PPP task asynchornously
    """
    serve_api = Serve3rdPartyAPI()
    serve_api.get_ppp_data()

