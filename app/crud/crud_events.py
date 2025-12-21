from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta
from app.models.events import Event
from app.models.clients import Client
from app.models.contracts import Contract
from app.models.users import User, Department


def create_event(db: Session, name: str, start_date: datetime, end_date: datetime,
                 location: str, attendees: int, notes: str, client_id: int,
                 contract_id: int, support_id: int = None):
    """Créer un nouvel événement"""
    # Validations
    if start_date >= end_date:
        raise ValueError("La date de fin doit être après la date de début")

    if attendees < 0:
        raise ValueError("Le nombre de participants ne peut pas être négatif")

    # Vérifier client
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise ValueError(f"Client ID {client_id} n'existe pas")

    # Vérifier contrat
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if not contract:
        raise ValueError(f"Contrat ID {contract_id} n'existe pas")

    if contract.client_id != client_id:
        raise ValueError("Le contrat n'appartient pas au client")

    if not contract.is_signed:
        raise ValueError("Le contrat doit être signé")

    # Vérifier support
    if support_id:
        support = db.query(User).filter(User.id == support_id).first()
        if not support:
            raise ValueError(f"Support ID {support_id} n'existe pas")

        if support.department != Department.SUPPORT:
            raise ValueError("L'utilisateur n'est pas du département SUPPORT")

    # Créer l'événement
    event = Event(
        name=name,
        start_date=start_date,
        end_date=end_date,
        location=location,
        attendees=attendees,
        notes=notes,
        client_id=client_id,
        contract_id=contract_id,
        support_id=support_id
    )

    db.add(event)
    db.commit()
    db.refresh(event)
    return event


def get_all_events(db: Session):
    """Obtenir tous les événements"""
    return db.query(Event).order_by(Event.start_date).all()


def get_event_by_id(db: Session, event_id: int):
    """Obtenir un événement par ID"""
    return db.query(Event).filter(Event.id == event_id).first()


def update_event(db: Session, event_id: int, **kwargs):
    """Mettre à jour un événement"""
    event = get_event_by_id(db, event_id)
    if not event:
        return None

    # Mettre à jour
    for key, value in kwargs.items():
        if hasattr(event, key):
            setattr(event, key, value)

    db.commit()
    db.refresh(event)
    return event


def delete_event(db: Session, event_id: int):
    """Supprimer un événement"""
    event = get_event_by_id(db, event_id)
    if not event:
        return None

    db.delete(event)
    db.commit()
    return event


def get_events_by_client(db: Session, client_id: int):
    """Obtenir les événements d'un client"""
    return db.query(Event).filter(Event.client_id == client_id).all()


def assign_support_to_event(db: Session, event_id: int, support_id: int):
    """Assigner un support à un événement"""
    # Vérifier que c'est un support
    support = db.query(User).filter(User.id == support_id).first()
    if not support or support.department != Department.SUPPORT:
        raise ValueError("L'utilisateur n'est pas du département SUPPORT")

    return update_event(db, event_id, support_id=support_id)


def get_events_without_support(db: Session):
    """Obtenir les événements sans support"""
    return db.query(Event).filter(Event.support_id == None).all()


def get_upcoming_events(db: Session, days: int = 7):
    """Obtenir les événements à venir"""
    future_date = datetime.now() + timedelta(days=days)
    return db.query(Event).filter(
        Event.start_date >= datetime.now(),
        Event.start_date <= future_date
    ).all()


def get_events_summary(db: Session):
    """Obtenir un résumé des événements"""
    now = datetime.now()

    total = db.query(func.count(Event.id)).scalar() or 0
    without_support = db.query(func.count(Event.id)).filter(Event.support_id == None).scalar() or 0
    upcoming = db.query(func.count(Event.id)).filter(Event.start_date > now).scalar() or 0
    ongoing = db.query(func.count(Event.id)).filter(
        Event.start_date <= now,
        Event.end_date >= now
    ).scalar() or 0

    return {
        'total': total,
        'without_support': without_support,
        'with_support': total - without_support,
        'upcoming': upcoming,
        'ongoing': ongoing,
        'past': total - upcoming - ongoing
    }


def get_events_by_support(db: Session, support_id: int):
    """Obtenir tous les événements d'un support spécifique"""
    return db.query(Event).filter(Event.support_id == support_id).all()


def get_events_by_date_range(db: Session, start_date: datetime, end_date: datetime):
    """Obtenir les événements dans une plage de dates"""
    return db.query(Event).filter(
        Event.start_date >= start_date,
        Event.end_date <= end_date
    ).order_by(Event.start_date).all()


def get_events_by_location(db: Session, location: str):
    """Obtenir les événements par lieu"""
    return db.query(Event).filter(Event.location.ilike(f"%{location}%")).all()


def search_events(db: Session, name: str = None, location: str = None,
                  client_id: int = None, support_id: int = None):
    """Recherche avancée d'événements"""
    query = db.query(Event)

    if name:
        query = query.filter(Event.name.ilike(f"%{name}%"))

    if location:
        query = query.filter(Event.location.ilike(f"%{location}%"))

    if client_id:
        query = query.filter(Event.client_id == client_id)

    if support_id:
        query = query.filter(Event.support_id == support_id)

    return query.order_by(Event.start_date).all()