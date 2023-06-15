"""
Common constants for the project
"""
import os
from pathlib import Path
from datetime import date
TODAY = date.today().strftime("%Y%m%d")

# BACKEND ######################################################################
LOG_DIR_NAME = "logs"
APP_LOG_FILE_NAME = "app.log"
DATA_DIR_NAME = "data"
FETCHED_DATA_NAME = "fetched"
GENERATED_DATA_NAME = "generated"
PPP_FILE_NAME = "ppp_data.csv"
EXCH_RATE_FILE_NAME= "exchange_rates.csv"
CURRENCY_FILE_NAME = "currencies.csv"
FINAL_MERGED_DATA_FILE_NAME = "final_merged_data.csv"


# Request tries for fetching data
REQUEST_TRY_COUNT = 5

# Paths
ROOTDIR = os.path.dirname(Path(os.path.abspath(__file__)))
VENVDIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)
LOG_TODAY_DIR = os.path.join(ROOTDIR, LOG_DIR_NAME, TODAY)
APP_LOG_FILE_PATH = os.path.join(LOG_TODAY_DIR, APP_LOG_FILE_NAME)
FETCHED_DATA_PATH = os.path.join(ROOTDIR, DATA_DIR_NAME, FETCHED_DATA_NAME)
GENERATED_DATA_PATH = os.path.join(ROOTDIR, DATA_DIR_NAME, GENERATED_DATA_NAME)


# Celery-related app config
CELERY_BROKER_URL = 'amqp://localhost'
CELERY_RESULT_BACKEND = 'rpc://' # old and deprecated soon
CELERY_LOG_FILE_NAME = "celery.log"
CELERY_LOG_FILE_PATH = os.path.join(LOG_TODAY_DIR, CELERY_LOG_FILE_NAME)