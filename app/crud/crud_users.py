from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.users import User, Department
from app.utils.auth import hash_password
from app.utils.validators import validate_email, validate_department


def create_user(db: Session, full_name: str, email: str, employee_id: str,
                password: str, department: str):
    """Créer un nouvel utilisateur"""
    # Validations
    if not validate_email(email):
        raise ValueError("Email invalide")

    if not validate_department(department):
        raise ValueError(f"Département invalide. Choisissez parmi: {[d.value for d in Department]}")

    # Vérifier unicité
    if db.query(User).filter(User.email == email).first():
        raise ValueError("Email déjà utilisé")

    if db.query(User).filter(User.employee_id == employee_id).first():
        raise ValueError("ID employé déjà utilisé")

    # Créer l'utilisateur
    user = User(
        full_name=full_name,
        email=email,
        employee_id=employee_id,
        hashed_password=hash_password(password),
        department=Department(department.upper())
    )

    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def get_all_users(db: Session):
    """Obtenir tous les utilisateurs"""
    return db.query(User).order_by(User.id).all()


def get_user_by_id(db: Session, user_id: int):
    """Obtenir un utilisateur par ID"""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    """Obtenir un utilisateur par email"""
    return db.query(User).filter(User.email == email).first()


def update_user(db: Session, user_id: int, **kwargs):
    """Mettre à jour un utilisateur"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    # Gérer le mot de passe
    if 'password' in kwargs:
        kwargs['hashed_password'] = hash_password(kwargs.pop('password'))

    # Mettre à jour
    for key, value in kwargs.items():
        if hasattr(user, key):
            setattr(user, key, value)

    db.commit()
    db.refresh(user)
    return user


def delete_user(db: Session, user_id: int):
    """Supprimer un utilisateur"""
    user = get_user_by_id(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user


def get_users_by_department(db: Session, department: Department):
    """Obtenir les utilisateurs par département"""
    return db.query(User).filter(User.department == department).all()


def get_sales_users(db: Session):
    """Obtenir tous les commerciaux"""
    return get_users_by_department(db, Department.SALES)


def get_support_users(db: Session):
    """Obtenir tous les supports"""
    return get_users_by_department(db, Department.SUPPORT)


def get_management_users(db: Session):
    """Obtenir tous les managers"""
    return get_users_by_department(db, Department.MANAGEMENT)


def get_users_summary(db: Session):
    """Obtenir un résumé des utilisateurs"""
    total = db.query(func.count(User.id)).scalar() or 0
    sales = db.query(func.count(User.id)).filter(User.department == Department.SALES).scalar() or 0
    support = db.query(func.count(User.id)).filter(User.department == Department.SUPPORT).scalar() or 0
    management = db.query(func.count(User.id)).filter(User.department == Department.MANAGEMENT).scalar() or 0

    return {
        'total': total,
        'sales': sales,
        'support': support,
        'management': management
    }
