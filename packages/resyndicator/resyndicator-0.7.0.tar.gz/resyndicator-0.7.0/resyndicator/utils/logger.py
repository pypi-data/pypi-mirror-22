import logging

logging.basicConfig(
    format='%(asctime)s: %(levelname)s: %(funcName)s: %(message)s')
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
