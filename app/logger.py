import logging

# from settings import LOG_PATH, LOG_BACKUPS, LOG_MAX_SIZE, LOG_LEVEL
from app.config import LOG_LEVEL

# from logging import handlers

handlers = [
    # handlers.RotatingFileHandler(LOG_PATH, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUPS),
    logging.StreamHandler(),
]

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    handlers=handlers,
)
