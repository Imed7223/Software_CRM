"""
Configuration de l'application
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


class Config:
    """Configuration de l'application"""
    # Base de données
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/epicevents")

    # Sécurité
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "ERROR")

    # Application
    APP_NAME = "Epicevents CRM"
    APP_VERSION = "1.0.0"

    @classmethod
    def validate(cls):
        """Valider la configuration"""
        errors = []

        if not cls.DATABASE_URL:
            errors.append("DATABASE_URL non défini")

        if not cls.SECRET_KEY or cls.SECRET_KEY == "dev-secret-key-change-in-production":
            errors.append("SECRET_KEY non sécurisé")

        if errors:
            raise ValueError(f"Erreurs de configuration: {', '.join(errors)}")

        return True