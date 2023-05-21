import logging 
from logging.handlers import RotatingFileHandler


logger = logging.getLogger(__name__)

file_handler = RotatingFileHandler(
    filename='logs/logs.log', 
    maxBytes=1024*4096, 
    backupCount=10, 
    encoding='utf-8'
)

strfmt = '[%(asctime)s] [%(levelname)s]: [%(message)s] [in %(pathname)s: line: %(lineno)d]'
datefmt = '%d.%m.%Y %H:%M:%S'

file_handler.setFormatter(logging.Formatter(fmt=strfmt, datefmt=datefmt))
file_handler.setLevel(logging.INFO)
logger.addHandler(file_handler)
logger.setLevel(logging.INFO)
