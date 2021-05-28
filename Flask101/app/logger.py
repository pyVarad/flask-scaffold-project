import logging
import logging.config
from flask_log_request_id import RequestIDLogFilter

logger = logging.getLogger(__name__)

def initialize_logging():
    handler = logging.StreamHandler()
    handler.setFormatter(
        logging.Formatter("%(asctime)s - %(name)s - level=%(levelname)s - request_id=%(request_id)s - %(message)s"))
    handler.addFilter(RequestIDLogFilter())  # << Add request id contextual filter
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.DEBUG)
    logging.getLogger('werkzeug').setLevel(logging.ERROR)