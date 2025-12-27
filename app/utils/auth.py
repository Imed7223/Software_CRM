# app/utils/auth.py

import os
from datetime import datetime, timedelta, UTC
import bcrypt
import jwt
from dotenv import load_dotenv
from sqlalchemy.orm import Session

from app.models.users import User, Department

load_dotenv()

# JWT / sécurité
SECRET_KEY = os.getenv("SECRET_KEY", "change_me")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "60"))


def authenticate_user(db: Session, email: str, password: str):
    """Authentifier un utilisateur par email / mot de passe."""
    user = db.query(User).filter(User.email == email).first()
    if not user:
        return None

    if verify_password(user.hashed_password, password):
        return user
    return None


def verify_password(hashed_password: str, password: str) -> bool:
    """Vérifier un mot de passe en le comparant au hash stocké."""
    return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))


def hash_password(password: str) -> str:
    """Hasher un mot de passe avec bcrypt."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def get_user_permissions(user: User):
    """Obtenir la liste des permissions d'un utilisateur selon son département."""
    permissions = {
        Department.SALES: [
            "view_clients",
            "manage_clients",
            "view_contracts",
            "create_contracts",
            "view_own_events",
        ],
        Department.SUPPORT: [
            "view_events",
            "manage_events",
            "view_clients",
            "view_contracts",
            "manage_own_events",
        ],
        Department.MANAGEMENT: [
            "view_all",
            "manage_all",
            "manage_users",
            "view_reports",
            "manage_permissions",
        ],
    }
    return permissions.get(user.department, [])


def has_permission(user: User, permission: str) -> bool:
    """Vérifier si un utilisateur possède une permission donnée."""
    return permission in get_user_permissions(user)


def require_permission(permission: str):
    """
    Décorateur pour vérifier les permissions dans les menus / fonctions.

    Usage :
        @require_permission("manage_users")
        def menu_users(user, db):
            ...
    """

    def decorator(func):
        def wrapper(user, *args, **kwargs):
            if not has_permission(user, permission):
                print("❌ Permission refusée. Accès non autorisé.")
                return None
            return func(user, *args, **kwargs)

        return wrapper

    return decorator


# ==== JWT pour la session CLI ====
def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Créer un jeton JWT contenant au moins :
      - sub : email de l'utilisateur
      - role : département (SALES / SUPPORT / MANAGEMENT)
      - user_id : id BDD
    """
    to_encode = data.copy()
    expire = datetime.now(UTC) + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict | None:
    """Décoder et vérifier un JWT, renvoie le payload ou None si invalide/expiré."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except jwt.ExpiredSignatureError:
        print("❌ Jeton expiré, veuillez vous reconnecter.")
    except jwt.InvalidTokenError:
        print("❌ Jeton invalide.")
    return None
