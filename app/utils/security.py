"""
Fonctions de sécurité avancées
"""
import os
from datetime import datetime, timedelta
from typing import Dict
from sqlalchemy.orm import Session
from app.crud import crud_users


class SecurityManager:
    """Gestionnaire de sécurité"""

    def __init__(self):
        self.login_attempts: Dict[str, Dict] = {}
        self.max_attempts = int(os.getenv('MAX_LOGIN_ATTEMPTS', '5'))
        self.lockout_duration = int(os.getenv('LOCKOUT_DURATION', '300'))  # 5 minutes

    def check_login_attempts(self, email: str) -> bool:
        """
        Vérifie si un utilisateur peut tenter de se connecter

        Args:
            email: Email de l'utilisateur

        Returns:
            True si la connexion est autorisée
        """
        if email not in self.login_attempts:
            return True

        attempts = self.login_attempts[email]

        # Vérifier si le lockout a expiré
        if attempts['locked_until'] and attempts['locked_until'] > datetime.now():
            remaining = (attempts['locked_until'] - datetime.now()).seconds // 60
            print(f"⚠️  Compte verrouillé. Réessayez dans {remaining} minutes")
            return False

        # Réinitialiser si le lockout a expiré
        if attempts['locked_until'] and attempts['locked_until'] <= datetime.now():
            del self.login_attempts[email]
            return True

        return attempts['count'] < self.max_attempts

    def record_failed_attempt(self, email: str):
        """
        Enregistre une tentative de connexion échouée
        """
        if email not in self.login_attempts:
            self.login_attempts[email] = {
                'count': 1,
                'last_attempt': datetime.now(),
                'locked_until': None
            }
        else:
            self.login_attempts[email]['count'] += 1
            self.login_attempts[email]['last_attempt'] = datetime.now()

            # Verrouiller le compte si trop de tentatives
            if self.login_attempts[email]['count'] >= self.max_attempts:
                lockout_time = datetime.now() + timedelta(seconds=self.lockout_duration)
                self.login_attempts[email]['locked_until'] = lockout_time
                print(f"🔒 Compte verrouillé pour {self.lockout_duration // 60} minutes")

    def record_successful_attempt(self, email: str):
        """
        Réinitialise les tentatives après une connexion réussie
        """
        if email in self.login_attempts:
            del self.login_attempts[email]

    @staticmethod
    def validate_session(last_activity: datetime) -> bool:
        """
        Valide une session utilisateur

        Args:
            last_activity: Dernière activité de l'utilisateur

        Returns:
            True si la session est valide
        """
        session_timeout = int(os.getenv('SESSION_TIMEOUT', '1800'))  # 30 minutes
        timeout_time = last_activity + timedelta(seconds=session_timeout)
        return datetime.now() <= timeout_time


# Instance globale
security_manager = SecurityManager()


def audit_log(db: Session, user_id: int, action: str, details: str = ""):
    """
    Journal d'audit des actions utilisateurs

    Args:
        db: Session de base de données
        user_id: ID de l'utilisateur
        action: Action effectuée
        details: Détails supplémentaires
    """
    user = crud_users.get_user_by_id(db, user_id)
    username = user.full_name if user else f"User {user_id}"

    log_entry = {
        'timestamp': datetime.now(),
        'user_id': user_id,
        'username': username,
        'action': action,
        'details': details,
        'ip_address': '127.0.0.1'  # À remplacer par l'IP réelle en production
    }

    # Log dans un fichier
    log_file = 'audit.log'
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"{log_entry['timestamp']} - {username} - {action} - {details}\n")

    print(f"📝 Audit: {username} - {action}")
