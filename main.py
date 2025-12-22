
"""
Software CRM - Application de gestion clientèle
Point d'entrée principal
"""
import os
import sys

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import init_db
from app.utils.logging_config import setup_logging, log_error
from app.menus.main_menu import main_menu


def init_app():
    """Initialise l'application"""
    try:
        # Configurer le logging
        logger = setup_logging()
        
        # Vérifier les variables d'environnement
        if not os.getenv("DATABASE_URL"):
            print("❌ ERREUR: DATABASE_URL non défini dans .env")
            print("⚠️  Créez un fichier .env avec la configuration de la base de données")
            sys.exit(1)
            
        if not os.getenv("SENTRY_DSN"):
            print("⚠️  SENTRY_DSN non défini - Sentry désactivé")
            
        print("=" * 50)
        print("      EPICEVENTS CRM - Gestion Clientèle")
        print("=" * 50)
        
        return logger
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)


if __name__ == "__main__":
    # Initialiser l'application
    logger = init_app()
    
    # Vérifier si les tables existent déjà
    from app.database.database import SessionLocal, engine
    from sqlalchemy import inspect
    
    db = SessionLocal()
    try:
        inspector = inspect(engine)
        tables_exist = inspector.get_table_names()
        
        if not tables_exist:
            print("🔄 Création des tables...")
            init_db()
            
            # Demander si on veut créer des données de démonstration
            response = input("📊 Voulez-vous créer des données de démonstration ? (o/n): ")
            if response.lower() == 'o':
                try:
                    from init_database import create_initial_data
                    create_initial_data()
                except ImportError:
                    print("⚠️  Fichier init_database.py non trouvé")
                except Exception as e:
                    log_error("Erreur création données démo", e)
                    print(f"❌ Erreur création données: {e}")
        else:
            print("✅ Base de données déjà initialisée")
            
    except Exception as e:
        log_error("Erreur vérification tables", e)
        print(f"❌ Erreur: {e}")
    finally:
        db.close()
    
    # Lancer le menu principal
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrompue")
    except Exception as e:
        log_error("Erreur dans le menu principal", e)
        print(f"❌ Erreur critique: {e}")