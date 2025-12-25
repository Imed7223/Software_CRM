"""
Software CRM - Application de gestion clientèle
Point d'entrée principal
"""
import os
import sys
from pathlib import Path

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import init_db, SessionLocal
from app.utils.logging_config import setup_logging, log_error
from app.menus.main_menu import main_menu
from app.utils.auth import authenticate_user, create_access_token, decode_access_token
from app.models.users import User


SESSION_FILE = os.path.join(Path.home(), ".crm_token")


def init_app():
    """Initialise l'application"""
    try:
        logger = setup_logging()

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


def load_session_user():
    """
    Récupérer le token dans ~/.crm_token et renvoyer l'utilisateur si valide.
    """
    if not os.path.exists(SESSION_FILE):
        return None

    try:
        with open(SESSION_FILE, "r", encoding="utf-8") as f:
            token = f.read().strip()

        payload = decode_access_token(token)
        if not payload:
            return None

        email = payload.get("sub")
        if not email:
            return None

        db = SessionLocal()
        try:
            user = db.query(User).filter(User.email == email).first()
            return db, user
        finally:
            # on ne ferme pas ici si on veut réutiliser db dans main_menu
            ...
    except Exception as e:
        log_error("Erreur chargement session", e)
        return None


def save_session_token(user: User):
    """
    Créer un JWT pour l'utilisateur et le stocker dans ~/.crm_token
    """
    token = create_access_token({
        "sub": user.email,
        "role": user.department.value,
        "user_id": user.id,
    })
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(token)


def clear_session():
    """Supprimer le fichier de session"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)


def login_flow():
    """
    Processus de connexion classique (email/mot de passe)
    Retourne (db, user) si OK, sinon (None, None)
    """
    db = SessionLocal()
    print("\n=== Connexion ===")
    email = input("Email: ")
    password = input("Mot de passe: ")

    user = authenticate_user(db, email, password)
    if user:
        print(f"\n✅ Bienvenue {user.full_name} ({user.department.value})")
        save_session_token(user)
        return db, user
    else:
        print("\n❌ Identifiants incorrects")
        db.close()
        return None, None


if __name__ == "__main__":
    # Initialiser l'application (logging, env, etc.)
    logger = init_app()

    # Ici tu peux appeler init_db() si tu veux créer les tables à la première exécution
    # init_db()

    # 1. Tenter de récupérer une session existante via JWT (~/.crm_token)
    session = load_session_user()
    if session:
        db, user = session
        if user:
            print(f"\n🔐 Session restaurée : {user.full_name} ({user.department.value})")
        else:
            # Token invalide / user supprimé
            db = None
            user = None
            clear_session()
    else:
        db = None
        user = None

    # 2. Si pas de session valide, lancer le process de connexion
    if not user:
        db, user = login_flow()
        if not user:
            sys.exit(1)

    # 3. Lancer le menu principal
    try:
        # main_menu attend normalement (db, user) ou fait son propre login
        # adapte si nécessaire
        main_menu()
    except KeyboardInterrupt:
        print("\n\n👋 Application interrompue")
    except Exception as e:
        log_error("Erreur dans le menu principal", e)
        print(f"❌ Erreur critique: {e}")
    finally:
        if db:
            db.close()
