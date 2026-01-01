"""
Software CRM - Application de gestion clientèle
Point d'entrée principal
"""
import os
import sys
from pathlib import Path

from app.menus.main_menu import main_menu
from app.utils.auth import authenticate_user, create_access_token
from app.models.users import User
from app.utils.security import security_manager  # tentatives login
from app.database.database import SessionLocal
from app.utils.logging_config import (
    setup_logging,
    log_error,
    log_info,
    log_warning,
    log_debug,
)

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

SESSION_FILE = os.path.join(Path.home(), ".crm_token")


def init_app():
    """Initialise l'application"""
    try:
        logger = setup_logging()
        log_info("Démarrage de l'application EPICEVENTS CRM")

        if not os.getenv("DATABASE_URL"):
            log_error("DATABASE_URL non défini dans .env")
            print("❌ ERREUR: DATABASE_URL non défini dans .env")
            print("⚠️  Créez un fichier .env avec la configuration de la base de données")
            sys.exit(1)

        if not os.getenv("SENTRY_DSN"):
            log_warning("SENTRY_DSN non défini - Sentry désactivé")
            print("⚠️  SENTRY_DSN non défini - Sentry désactivé")
        else:
            log_debug("SENTRY_DSN détecté, Sentry actif")

        print("=" * 50)
        print("      EPICEVENTS CRM - Gestion Clientèle")
        print("=" * 50)

        return logger

    except Exception as e:
        log_error("Erreur lors de l'initialisation de l'application", e)
        print(f"❌ Erreur lors de l'initialisation: {e}")
        sys.exit(1)


def save_session_token(user: User):
    """
    Créer un JWT pour l'utilisateur et le stocker dans ~/.crm_token
    (utilisé pour démo / debug, mais pas pour restaurer automatiquement la session)
    """
    token = create_access_token({
        "sub": user.email,
        "role": user.department.value,
        "user_id": user.id,
    })
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(token)
    log_debug(f"Token de session sauvegardé pour {user.email} dans {SESSION_FILE}")


def clear_session():
    """Supprimer le fichier de session (si besoin)"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        log_info("Fichier de session ~/.crm_token supprimé")


def login_flow():
    """
    Processus de connexion classique (email/mot de passe)
    Retourne (db, user) si OK, sinon (None, None)
    """
    db = SessionLocal()
    print("\n=== Connexion ===")
    email = input("Email: ")

    # Vérifier le nombre de tentatives (SecurityManager)
    if not security_manager.check_login_attempts(email):
        db.close()
        return None, None

    password = input("Mot de passe: ")

    user = authenticate_user(db, email, password)
    if user:
        print(f"\n✅ Bienvenue {user.full_name} ({user.department.value})")
        log_info(f"Connexion réussie pour {email}")
        security_manager.record_successful_attempt(email)
        # On génère et stocke quand même un JWT (pour démo / audit)
        save_session_token(user)
        return db, user
    else:
        print("\n❌ Identifiants incorrects")
        log_warning(f"Tentative de connexion échouée pour {email}")
        security_manager.record_failed_attempt(email)
        db.close()
        return None, None


if __name__ == "__main__":
    # Optionnel : si on passe "login" en argument, on force la suppression du token
    force_login = len(sys.argv) > 1 and sys.argv[1] == "login"
    logger = init_app()

    if force_login:
        clear_session()

    db, user = login_flow()
    if not user:
        sys.exit(1)

    # Lancer le menu principal
    try:
        main_menu(db, user)
    except KeyboardInterrupt:
        print("\n\n👋 Application interrompue")
    except Exception as e:
        log_error("Erreur dans le menu principal", e)
        print(f"❌ Erreur critique: {e}")
    finally:
        if db:
            db.close()
