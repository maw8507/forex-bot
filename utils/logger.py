
import logging

logger = logging.getLogger("forex_bot")
logger.setLevel(logging.INFO)
ch = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s — %(levelname)s — %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
