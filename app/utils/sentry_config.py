"""
Configuration Sentry pour la journalisation et la surveillance des erreurs
"""

import logging
import os

import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration


def init_sentry():
    """
    Initialise Sentry pour la surveillance des erreurs
    """
    sentry_dsn = os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        print("⚠️  SENTRY_DSN non configuré - Journalisation Sentry désactivée")
        return

    # Intégration du logging Python
    sentry_logging = LoggingIntegration(
        level=logging.INFO,       # Capturer les logs à partir de INFO
        event_level=logging.ERROR # Envoyer à Sentry à partir de ERROR
    )

    sentry_sdk.init(
        dsn=sentry_dsn,  # ✅ DSN chargé depuis le fichier .env
        integrations=[
            sentry_logging,
            SqlalchemyIntegration(),
        ],
        # Performance monitoring (à réduire en production si nécessaire)
        traces_sample_rate=1.0,
        # Ne pas envoyer de données personnelles par défaut
        send_default_pii=False,
        # Environnement (development, staging, production)
        environment=os.getenv("ENVIRONMENT", "development"),
        # Version de l'application
        release=os.getenv("APP_VERSION", "1.0.0"),
    )

    print("✅ Sentry initialisé pour la surveillance des erreurs")


def capture_exception(exception: Exception, context: dict | None = None):
    """
    Capture une exception et l'envoie à Sentry

    Args:
        exception: Exception à capturer
        context: Dictionnaire de contexte supplémentaire
    """
    try:
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_extra(key, value)
            sentry_sdk.capture_exception(exception)
    except Exception as e:
        # Fallback si Sentry échoue
        print(f"⚠️  Erreur lors de l'envoi de l'exception à Sentry: {e}")


def capture_message(message: str, level: str = "error"):
    """
    Capture un message et l'envoie à Sentry

    Args:
        message: Message à capturer
        level: Niveau du message (debug, info, warning, error)
    """
    try:
        sentry_sdk.capture_message(message, level=level)
    except Exception as e:
        print(f"⚠️  Erreur lors de l'envoi du message à Sentry: {e}")
