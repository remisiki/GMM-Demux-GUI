import os
import sys
import subprocess
from logging import getLogger
logger = getLogger(__name__)

def openFileInSystem(file):
    if (not file):
        logger.error("Empty file path.")
        return
    try:
        if sys.platform == 'linux':
            subprocess.Popen(['xdg-open', file])
        elif sys.platform == 'win32':
            os.startfile(file)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', file])
    except Exception:
        logger.error(f"Bad file open request on {sys.platform}, file: {file}.")
        return

    logger.info(f"Opened {file}.")