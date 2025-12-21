import logging
import os
import sys

from sentry_sdk import capture_message

from .sentry_config import init_sentry, capture_exception


# Logger global
_logger = None


def get_logger():
    global _logger
    if _logger is None:
        _logger = SentryAwareLogger("epicevents")
    return _logger


def log_info(message: str):
    get_logger().info(message)


def log_warning(message: str):
    get_logger().warning(message)


def log_error(message: str, exception: Exception = None):
    get_logger().error(message, exc_info=exception)


def log_debug(message: str):
    get_logger().debug(message)


def setup_logging():
    """Configurer le logging et Sentry"""
    log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()

    # Configuration de base
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler('epicevents_crm.log', encoding='utf-8')
        ]
    )

    # Initialiser Sentry
    init_sentry()

    # Désactiver SQLAlchemy logs sauf si DEBUG
    if log_level != 'DEBUG':
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)

    logger = logging.getLogger('epicevents')
    logger.info(f"Logging configuré avec le niveau: {log_level}")

    return logger


class SentryAwareLogger:
    """Logger qui envoie aussi les erreurs à Sentry"""

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def error(self, msg, *args, exc_info=None, **kwargs):
        self.logger.error(msg, *args, exc_info=exc_info, **kwargs)
        if exc_info and isinstance(exc_info, Exception):
            capture_exception(exc_info, {'message': msg})
        elif exc_info:
            capture_message(f"{msg} - {exc_info}", level="error")

    def critical(self, msg, *args, exc_info=None, **kwargs):
        self.logger.critical(msg, *args, exc_info=exc_info, **kwargs)
        if exc_info:
            capture_message(msg, level="error")

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)
        capture_message(msg, level="warning")

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)