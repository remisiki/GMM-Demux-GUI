import sys
import json
import app.index
import app.logger
import traceback
from logging import getLogger
logger = getLogger(__name__)

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(f"GMM-demux exited unexpectedly. {tb}")
    sys.exit(-1)

if __name__ == "__main__":
    sys.excepthook = excepthook
    app.index.main()