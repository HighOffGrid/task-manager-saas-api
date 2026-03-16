import logging
from pythonjsonlogger import jsonlogger

logger = logging.getLogger()
logger.setLevel(logging.INFO)

logHandler = logging.StreamHandler()

formatter = jsonlogger.JsonFormatter(
    "%(asctime)s %(levelname)s %(message)s"
)

fileHandler = logging.FileHandler("app.log")

fileHandler.setFormatter(formatter)

logger.addHandler(fileHandler)