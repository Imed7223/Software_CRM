"""
Configuration Sentry pour la journalisation des erreurs
"""
import logging

import sentry_sdk
import os
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.integrations.logging import LoggingIntegration


def init_sentry():
    """
    Initialise Sentry pour la surveillance des erreurs
    """
    sentry_dsn = os.getenv("SENTRY_DSN")

    if not sentry_dsn:
        print("⚠️  SENTRY_DSN non configuré - Journalisation Sentry désactivée")
        return

    # Capturer tous les niveaux de log
    sentry_logging = LoggingIntegration(
        level=logging.INFO,  # Capturer les logs à partir d'INFO
        event_level=logging.ERROR  # Envoyer à Sentry à partir d'ERROR
    )

    sentry_sdk.init(
        dsn=sentry_dsn,
        integrations=[
            sentry_logging,
            SqlalchemyIntegration(),
        ],
        # Performance monitoring
        traces_sample_rate=1.0,
        # Debug info
        send_default_pii=False,
        # Environnement
        environment=os.getenv("ENVIRONMENT", "development"),
        release=os.getenv("APP_VERSION", "1.0.0"),
    )

    print("✅ Sentry initialisé pour la surveillance des erreurs")


def capture_exception(exception: Exception, context: dict = None):
    """
    Capture une exception et l'envoie à Sentry

    Args:
        exception: Exception à capturer
        context: Contexte supplémentaire
    """
    try:
        with sentry_sdk.push_scope() as scope:
            if context:
                for key, value in context.items():
                    scope.set_extra(key, value)
            sentry_sdk.capture_exception(exception)
    except Exception as e:
        # Fallback en cas d'échec Sentry
        print(f"⚠️  Erreur lors de l'envoi à Sentry: {e}")


def capture_message(message: str, level: str = "error"):
    """
    Capture un message et l'envoie à Sentry

    Args:
        message: Message à capturer
        level: Niveau (debug, info, warning, error)
    """
    try:
        sentry_sdk.capture_message(message, level=level)
    except Exception as e:
        print(f"⚠️  Erreur Sentry: {e}")