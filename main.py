
"""
Software CRM - Application de gestion clientèle
Point d'entrée principal
"""
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.utils.logging_config import setup_logging
from app.menus.main_menu import main_menu


def init_app():
    """Initialise l'application"""
    # Configurer le logging
    setup_logging()

    # Vérifier les variables d'environnement
    if not os.getenv("DATABASE_URL"):
        print("❌ ERREUR: DATABASE_URL non défini dans .env")
        print("⚠️  Créez un fichier .env avec la configuration de la base de données")
        sys.exit(1)

    print("=" * 50)
    print("      EPICEVENTS CRM - Gestion Clientèle")
    print("=" * 50)


if __name__ == "__main__":
    init_app()
    main_menu()
