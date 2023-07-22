import logging

from app.config import LOG_LEVEL


handlers = [
    # handlers.RotatingFileHandler(LOG_PATH, maxBytes=LOG_MAX_SIZE, backupCount=LOG_BACKUPS),
    logging.StreamHandler(),
]

logging.basicConfig(
    level=LOG_LEVEL,
    format="%(asctime)s %(levelname)s [%(filename)s.%(funcName)s:%(lineno)d] %(message)s",
    handlers=handlers,
)
