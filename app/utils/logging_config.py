import logging
import os
import sys


def setup_logging():
    """Configurer le logging de l'application"""
    # Niveau de log depuis l'environnement
    log_level = os.getenv('LOG_LEVEL', 'ERROR').upper()

    # Configuration de base
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Désactiver SQLAlchemy logs
    if log_level != 'DEBUG':
        logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)
        logging.getLogger('sqlalchemy.pool').setLevel(logging.ERROR)

    return logging.getLogger('epicevents')