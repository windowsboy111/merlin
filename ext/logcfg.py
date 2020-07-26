import logging
import logging.config


def get_logger(loggerName):
    logger = logging.getLogger(loggerName)
    logger.setLevel(logging.INFO)
    handler = logging.FileHandler(filename='discordbot.log', encoding='utf-8', mode='w')
    handler.setFormatter(logging.Formatter('[%(asctime)s]%(levelname)s - %(name)s: %(message)s'))
    logger.addHandler(handler)
    return logger
