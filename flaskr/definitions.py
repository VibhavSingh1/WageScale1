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

# Paths
ROOTDIR = os.path.dirname(Path(os.path.abspath(__file__)))
VENVDIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)
LOG_TODAY_DIR = os.path.join(ROOTDIR, LOG_DIR_NAME, TODAY)
APP_LOG_FILE_PATH = os.path.join(LOG_TODAY_DIR, APP_LOG_FILE_NAME)
FETCHED_DATA_PATH = os.path.join(ROOTDIR, DATA_DIR_NAME, FETCHED_DATA_NAME)


