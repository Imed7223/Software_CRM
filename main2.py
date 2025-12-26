"""
Software CRM - Application de gestion clientèle
Point d'entrée principal
"""
import os
import sys
from pathlib import Path

import click
from rich.console import Console

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database.database import init_db, SessionLocal
from app.utils.logging_config import (
    setup_logging,
    log_error,
    log_info,
    log_warning,
    log_debug,
)
from app.menus.main_menu import main_menu
from app.utils.auth import authenticate_user, create_access_token, decode_access_token
from app.models.users import User
from app.utils.security import security_manager  # SecurityManager (tentatives login)
from init_database import create_initial_data  # script de données de démo

SESSION_FILE = os.path.join(Path.home(), ".crm_token")

console = Console()
logger = None  # sera initialisé dans init_app()


def init_app():
    """Initialise l'application (logging, .env, vérifs de base)."""
    global logger
    try:
        logger = setup_logging()
        log_info("Démarrage de l'application EPICEVENTS CRM")

        if not os.getenv("DATABASE_URL"):
            log_error("DATABASE_URL non défini dans .env")
            console.print("[bold red]❌ ERREUR: DATABASE_URL non défini dans .env[/bold red]")
            console.print("⚠️  Créez un fichier .env avec la configuration de la base de données")
            sys.exit(1)

        if not os.getenv("SENTRY_DSN"):
            log_warning("SENTRY_DSN non défini - Sentry désactivé")
            console.print("[yellow]⚠️  SENTRY_DSN non défini - Sentry désactivé[/yellow]")
        else:
            log_debug("SENTRY_DSN détecté, Sentry actif")

        console.print("=" * 50)
        console.print("[bold magenta]      EPICEVENTS CRM - Gestion Clientèle[/bold magenta]")
        console.print("=" * 50)

    except Exception as e:
        log_error("Erreur lors de l'initialisation de l'application", e)
        console.print(f"[bold red]❌ Erreur lors de l'initialisation: {e}[/bold red]")
        sys.exit(1)


def load_session_user():
    """
    Récupérer le token dans ~/.crm_token et renvoyer (db, user) si valide.
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
        user = db.query(User).filter(User.email == email).first()
        if not user:
            log_warning(f"Utilisateur pour le token JWT introuvable: {email}")
            db.close()
            return None

        return db, user

    except Exception as e:
        log_error("Erreur chargement session", e)
        return None


def save_session_token(user: User):
    """
    Créer un JWT pour l'utilisateur et le stocker dans ~/.crm_token
    """
    token = create_access_token(
        {
            "sub": user.email,
            "role": user.department.value,
            "user_id": user.id,
        }
    )
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(token)
    log_debug(f"Token de session sauvegardé pour {user.email} dans {SESSION_FILE}")


def clear_session():
    """Supprimer le fichier de session"""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        log_info("Fichier de session ~/.crm_token supprimé")


def login_flow():
    """
    Processus de connexion classique (email/mot de passe)
    Retourne (db, user) si OK, sinon (None, None)
    """
    db = SessionLocal()
    console.print("\n[bold cyan]=== Connexion ===[/bold cyan]")
    email = input("Email: ")

    # Vérifier le nombre de tentatives (SecurityManager)
    if not security_manager.check_login_attempts(email):
        db.close()
        return None, None

    password = input("Mot de passe: ")

    user = authenticate_user(db, email, password)
    if user:
        console.print(f"\n[bold green]✅ Bienvenue {user.full_name} ({user.department.value})[/bold green]")
        log_info(f"Connexion réussie pour {email}")
        security_manager.record_successful_attempt(email)
        save_session_token(user)
        return db, user
    else:
        console.print("\n[bold red]❌ Identifiants incorrects[/bold red]")
        log_warning(f"Tentative de connexion échouée pour {email}")
        security_manager.record_failed_attempt(email)
        db.close()
        return None, None


# ==========================
#   CLI CLICK (login / init)
# ==========================

@click.group()
def cli():
    """EpicEvents CRM - Interface en ligne de commande."""
    # Initialisation commune (logs, .env, etc.)
    init_app()


@cli.command()
def init_db_cmd():
    """
    Créer les tables et initialiser la base avec des données de démonstration.
    """
    console.print("[bold cyan]🔧 Création des tables...[/bold cyan]")
    init_db()
    console.print("[bold cyan]🔄 Insertion des données de démonstration...[/bold cyan]")
    try:
        create_initial_data()
        console.print("[bold green]✅ Base initialisée avec succès.[/bold green]")
    except Exception as e:
        console.print(f"[bold red]❌ Erreur lors de l'initialisation : {e}[/bold red]")


@cli.command()
def login():
    """
    Connexion d'un utilisateur et lancement du menu principal.
    Commande demandée par le cahier des charges : `python main.py login`.
    """
    # 1. Tenter de restaurer une session existante
    session = load_session_user()
    if session:
        db, user = session
        console.print(
            f"\n[bold yellow]🔐 Session restaurée : {user.full_name} ({user.department.value})[/bold yellow]"
        )
        log_info(f"Session restaurée pour {user.email}")
    else:
        db = None
        user = None

    # 2. Si pas de session valide, lancer le process de connexion
    if not user:
        db, user = login_flow()
        if not user:
            # échec de connexion
            sys.exit(1)

    # 3. Lancer le menu principal
    try:
        # attention : main_menu doit accepter (db, user)
        main_menu(db, user)
    except KeyboardInterrupt:
        console.print("\n\n👋 Application interrompue")
    except Exception as e:
        log_error("Erreur dans le menu principal", e)
        console.print(f"[bold red]❌ Erreur critique: {e}[/bold red]")
    finally:
        if db:
            db.close()


if __name__ == "__main__":
    cli()