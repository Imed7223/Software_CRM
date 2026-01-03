"""
Software CRM - Application de gestion clientèle
Point d'entrée principal
"""
import os
import sys

from app.menus.main_menu import main_menu
from app.utils.auth import (
    authenticate_user,
    create_access_token,
    decode_access_token,
)
from app.crud.crud_users import get_user_by_email
from app.utils.security import security_manager  # tentatives login
from app.database.database import SessionLocal
from app.utils.logging_config import (
    setup_logging,
    log_error,
    log_info,
    log_warning,
    log_debug,
)
from app.utils.session import (
    save_session_token,
    load_session_token,
    clear_session,
)

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


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

        # Générer un JWT et le sauvegarder pour restaurer la session plus tard
        token = create_access_token({
            "sub": user.email,
            "role": user.department.value,
            "user_id": user.id,
        })
        save_session_token(token, user.email)

        return db, user
    else:
        print("\n❌ Identifiants incorrects")
        log_warning(f"Tentative de connexion échouée pour {email}")
        security_manager.record_failed_attempt(email)
        db.close()
        return None, None


def load_session_user(db):
    """
    Tente de restaurer une session à partir du fichier ~/.crm_token.
    Retourne un User ou None.
    """
    token = load_session_token()
    if not token:
        return None

    try:
        payload = decode_access_token(token)
        if not payload:
            # decode_access_token affiche déjà le message (expiré / invalide)
            clear_session()
            return None

        email = payload.get("sub")
        if not email:
            return None

        user = get_user_by_email(db, email)
        if not user:
            return None

        log_info(f"Session restaurée pour {email} depuis le token")
        return user

    except Exception as e:
        log_error("Erreur lors de la restauration de session", e)
        print(f"🔑 Erreur lors de la restauration de session: {e}")
        return None


if __name__ == "__main__":
    logger = init_app()

    db = SessionLocal()
    user = load_session_user(db)  # tente de restaurer la session

    if not user:
        # pas de session valide → login classique
        db.close()
        db, user = login_flow()

    if not user:
        sys.exit(1)

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
