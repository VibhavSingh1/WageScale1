"""
Common constants for the project
"""
import os
from pathlib import Path

# BACKEND ######################################################################

# Paths
ROOTDIR = os.path.dirname(Path(os.path.abspath(__file__)))
VENVDIR = os.path.dirname(Path(os.path.abspath(__file__)).parent)
