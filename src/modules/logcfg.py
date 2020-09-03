import logging
import logging.config


def get_logger(loggerName):
    logger = logging.getLogger(loggerName)
    return logger
