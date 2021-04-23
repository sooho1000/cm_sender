import logging

logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)
formatter = logging.Formatter('[%(asctime)s][%(levelname)s|%(filename)s:%(lineno)s] >> %(message)s')
streamHandler = logging.StreamHandler()
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)
logger.setLevel(level=logging.INFO)

def get_logger():
    logger = logging.getLogger(__name__)
    return logger