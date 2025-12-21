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


def require_permission(permission: str):
    """
    Décorateur pour vérifier les permissions dans les menus

    Args:
        permission: Permission requise

    Returns:
        function: Décorateur
    """

    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if not has_permission(user, permission):
                print(f"❌ Permission refusée. Accès non autorisé.")
                return None
            return func(user, *args, **kwargs)

        return wrapper

    return decorator


def check_permission(user: User, permission: str) -> bool:
    """
    Vérifie si l'utilisateur a une permission spécifique

    Args:
        user: Utilisateur à vérifier
        permission: Permission requise

    Returns:
        True si l'utilisateur a la permission
    """
    return has_permission(user, permission)