import logging
import os
from logging.handlers import RotatingFileHandler

os.makedirs("logs", exist_ok=True)

file_handler = RotatingFileHandler(
    "logs/data_migration.log",
    maxBytes=1_000_000,
    backupCount=3
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    handlers=[
        file_handler,
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("data_migration")