import logging.handlers
import os

from Flask_Auto_Translate.config_loader import config

MAX_LOG_SIZE_MB = config["DEFAULT"].getint("MAX_LOG_SIZE_MB")
MAX_LOG_BACKUP_COUNT = config["DEFAULT"].getint("MAX_LOG_BACKUP_COUNT")
LOG_LEVEL = config['DEFAULT']['LOG_LEVEL']

# dir of log
log_dir_path = "log"
if not os.path.isdir(log_dir_path):
    os.mkdir(log_dir_path)

logger_handler = logging.handlers.RotatingFileHandler(
    f"{log_dir_path}/Flask_Auto_Translate.log",
    mode='a', maxBytes=1024 * 1024 * MAX_LOG_SIZE_MB,
    backupCount=MAX_LOG_BACKUP_COUNT,
    encoding=None, delay=False)
logger_handler.setFormatter(logging.Formatter(
    '[%(asctime)s] %(levelname)s in %(module)s: %(message)s'))

logger = logging.getLogger(__name__)
logger.addHandler(logger_handler)
logger.setLevel(LOG_LEVEL)
