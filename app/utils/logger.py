import logging
from app.core.config import settings

def create_logging(name: str):
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s [%(levelname)s] %(message)s - %(pathname)s:%(lineno)d",
        handlers=[
            logging.FileHandler(settings.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(name)

logger = create_logging("procon")
