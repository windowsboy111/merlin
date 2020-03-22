import logging
import logging.config

logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='G:/my drive/coding/python/log/discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('[%(asctime)s]%(levelname)s - %(name)s: %(message)s'))
logger.addHandler(handler)
