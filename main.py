import sys
import json
import app.index
import traceback
from logging import config, getLogger

def excepthook(exc_type, exc_value, exc_tb):
    tb = "".join(traceback.format_exception(exc_type, exc_value, exc_tb))
    logger.error(f"GMM-demux exited unexpectedly. {tb}")
    sys.exit(-1)

if __name__ == "__main__":

    sys.excepthook = excepthook

    with open('log_config.json', 'r') as f:
        log_conf = json.load(f)
        config.dictConfig(log_conf)
    logger = getLogger(__name__)

    app.index.main()