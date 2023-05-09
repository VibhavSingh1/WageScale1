"""
Common constants for the project
"""
import os
from pathlib import Path
from urllib.parse import urljoin

# BACKEND ######################################################################
# FileAND Dir Names
TEMPLATE_NAME = "templates"
STATIC_DIR_NAME = "static"
IMAGES_DIR_NAME = "images"
CSS_DIR_NAME = "css"


TEMPLATE_NAME_HOME = "index.html"  # home, index, /
TEMPLATE_NAME_ABOUT = "about.html"

BACKGROUND_IMG_NAME = "background1.jpg"

# Paths
ROOTDIR = os.path.dirname(Path(os.path.abspath(__file__)))
VENVDIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)

TEMPLATE_DIR_PATH = os.path.join(
    ROOTDIR,
    TEMPLATE_NAME,
)

# BACKGROUND_IMG_PATH = os.path.join(
#     STATIC_DIR_NAME,
#     IMAGES_DIR_NAME,
#     BACKGROUND_IMG_NAME,
# )

# # FRONTEND ######################################################################
# # Page names
# PAGE_ABOUT = "about"
# PAGE_HOME = "home"
# PAGE_INDEX = "index"

# Page URLs
# URL_HOME_1 = "/"
# URL_HOME_2 = urljoin(URL_HOME_1, PAGE_INDEX)
# URL_HOME_3 = urljoin(URL_HOME_1, PAGE_HOME)
# URL_ABOUT = urljoin(URL_HOME_1, PAGE_ABOUT)
# URL_BACKGROUND_IMG = urljoin(URL_HOME_1, BACKGROUND_IMG_PATH)
