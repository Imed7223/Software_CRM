import os
from pathlib import Path

from app.utils.logging_config import log_info, log_debug

SESSION_FILE = os.path.join(Path.home(), ".crm_token")


def save_session_token(token: str, email: str):
    """Sauvegarder le token JWT dans ~/.crm_token."""
    with open(SESSION_FILE, "w", encoding="utf-8") as f:
        f.write(token)
    log_debug(f"Token de session sauvegardé pour {email} dans {SESSION_FILE}")


def load_session_token() -> str | None:
    """Lire le token depuis ~/.crm_token, ou None s'il n'existe pas."""
    if not os.path.exists(SESSION_FILE):
        return None
    with open(SESSION_FILE, "r", encoding="utf-8") as f:
        token = f.read().strip()
    return token or None


def clear_session():
    """Supprimer le fichier de session (si besoin)."""
    if os.path.exists(SESSION_FILE):
        os.remove(SESSION_FILE)
        log_info("Fichier de session ~/.crm_token supprimé")
