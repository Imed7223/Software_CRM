from sqlalchemy.orm import Session
from datetime import datetime
from app.models.clients import Client
from app.models.users import User
from app.utils.validators import validate_email, validate_phone


def create_client(db: Session, full_name: str, email: str, phone: str,
                  company_name: str, commercial_id: int):
    """Créer un nouveau client"""
    # Validations
    if not validate_email(email):
        raise ValueError("Email invalide")

    if phone and not validate_phone(phone):
        raise ValueError("Numéro de téléphone invalide")

    # Vérifier que le commercial existe
    commercial = db.query(User).filter(User.id == commercial_id).first()
    if not commercial:
        raise ValueError(f"Commercial ID {commercial_id} n'existe pas")

    # Créer le client
    client = Client(
        full_name=full_name,
        email=email,
        phone=phone,
        company_name=company_name,
        commercial_id=commercial_id,
        created_date=datetime.now(),
        last_contact=datetime.now()
    )

    db.add(client)
    db.commit()
    db.refresh(client)
    return client


def get_all_clients(db: Session):
    """Obtenir tous les clients"""
    return db.query(Client).order_by(Client.id).all()


def get_client_by_id(db: Session, client_id: int):
    """Obtenir un client par ID"""
    return db.query(Client).filter(Client.id == client_id).first()


def update_client(db: Session, client_id: int, **kwargs):
    """Mettre à jour un client"""
    client = get_client_by_id(db, client_id)
    if not client:
        return None

    # Mettre à jour
    for key, value in kwargs.items():
        if hasattr(client, key):
            setattr(client, key, value)

    client.last_contact = datetime.now()
    db.commit()
    db.refresh(client)
    return client


def delete_client(db: Session, client_id: int):
    """Supprimer un client"""
    client = get_client_by_id(db, client_id)
    if not client:
        return None

    db.delete(client)
    db.commit()
    return client


def get_clients_by_commercial(db: Session, commercial_id: int):
    """Obtenir les clients d'un commercial"""
    return db.query(Client).filter(Client.commercial_id == commercial_id).all()


def search_clients(db: Session, name: str = None, company: str = None,
                   email: str = None, commercial_id: int = None):
    """Recherche avancée de clients"""
    query = db.query(Client)

    if name:
        query = query.filter(Client.full_name.ilike(f"%{name}%"))

    if company:
        query = query.filter(Client.company_name.ilike(f"%{company}%"))

    if email:
        query = query.filter(Client.email.ilike(f"%{email}%"))

    if commercial_id:
        query = query.filter(Client.commercial_id == commercial_id)

    return query.order_by(Client.full_name).all()


def get_clients_without_contract(db: Session):
    """Obtenir les clients sans contrat"""
    return db.query(Client).filter(~Client.contracts.any()).all()


def get_clients_last_contact_before(db: Session, days: int = 30):
    """Obtenir les clients sans contact depuis X jours"""
    from datetime import datetime, timedelta
    cutoff_date = datetime.now() - timedelta(days=days)
    return db.query(Client).filter(Client.last_contact <= cutoff_date).all()
