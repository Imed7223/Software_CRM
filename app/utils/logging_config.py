import logging
import os
import sys
from .sentry_config import init_sentry, capture_exception

def setup_logging():
    """Configurer le logging et Sentry"""
    log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()
    
    # Initialiser Sentry
    init_sentry()
    
    # Configuration de base
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        handlers=[
            logging.StreamHandler(sys.stdout),
        ]
    )
    
    # Désactiver SQLAlchemy logs sauf si DEBUG
    if log_level != 'DEBUG':
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
    
    logger = logging.getLogger('epicevents')
    logger.info(f"Logging configuré avec le niveau: {log_level}")
    
    return logger

def log_error(message: str, exception: Exception = None):
    """Log une erreur"""
    logger = logging.getLogger('epicevents')
    if exception:
        logger.error(f"{message}: {exception}", exc_info=True)
        capture_exception(exception, {'message': message})
    else:
        logger.error(message)

def log_info(message: str):
    """Log un message informatif"""
    logger = logging.getLogger('epicevents')
    logger.info(message)

def log_warning(message: str):
    """Log un avertissement"""
    logger = logging.getLogger('epicevents')
    logger.warning(message)
    # Optionnel : envoyer à Sentry aussi
    from .sentry_config import capture_message
    capture_message(message, level="warning")

def log_debug(message: str):
    """Log un message de debug"""
    logger = logging.getLogger('epicevents')
    logger.debug(message)