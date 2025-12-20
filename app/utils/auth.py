from sqlalchemy.orm import Session
import bcrypt
from app.models.users import User, Department


def authenticate_user(db: Session, email: str, password: str):
    """Authentifier un utilisateur"""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if verify_password(user.hashed_password, password):
        return user
    return None


def verify_password(hashed_password: str, password: str):
    """Vérifier un mot de passe"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))


def hash_password(password: str):
    """Hasher un mot de passe"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')


def get_user_permissions(user: User):
    """Obtenir les permissions d'un utilisateur"""
    permissions = {
        Department.SALES: [
            'view_clients', 'manage_clients',
            'view_contracts', 'create_contracts',
            'view_own_events'
        ],
        Department.SUPPORT: [
            'view_events', 'manage_events',
            'view_clients', 'view_contracts',
            'manage_own_events'
        ],
        Department.MANAGEMENT: [
            'view_all', 'manage_all', 'manage_users',
            'view_reports', 'manage_permissions'
        ]
    }

    return permissions.get(user.department, [])


def has_permission(user: User, permission: str):
    """Vérifier si un utilisateur a une permission"""
    return permission in get_user_permissions(user)