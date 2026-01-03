from sqlalchemy.orm import Session
from sqlalchemy import func
from app.models.contracts import Contract
from app.models.clients import Client
from app.models.users import User


def create_contract(db: Session, total_amount: float, remaining_amount: float,
                    is_signed: bool, client_id: int, commercial_id: int):
    """Créer un nouveau contrat"""
    # Vérifications
    if remaining_amount > total_amount:
        raise ValueError("Le montant restant ne peut pas dépasser le montant total")

    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise ValueError(f"Client ID {client_id} n'existe pas")

    commercial = db.query(User).filter(User.id == commercial_id).first()
    if not commercial:
        raise ValueError(f"Commercial ID {commercial_id} n'existe pas")

    # Créer le contrat
    contract = Contract(
        total_amount=total_amount,
        remaining_amount=remaining_amount,
        is_signed=is_signed,
        client_id=client_id,
        commercial_id=commercial_id
    )

    db.add(contract)
    db.commit()
    db.refresh(contract)
    return contract


def get_all_contracts(db: Session):
    """Obtenir tous les contrats"""
    return db.query(Contract).order_by(Contract.id).all()


def get_contract_by_id(db: Session, contract_id: int):
    """Obtenir un contrat par ID"""
    return db.query(Contract).filter(Contract.id == contract_id).first()


def update_contract(db: Session, contract_id: int, **kwargs):
    """Mettre à jour un contrat"""
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    # Validation des montants
    if 'total_amount' in kwargs or 'remaining_amount' in kwargs:
        new_total = kwargs.get('total_amount', contract.total_amount)
        new_remaining = kwargs.get('remaining_amount', contract.remaining_amount)

        if new_remaining > new_total:
            raise ValueError("Le montant restant ne peut pas dépasser le montant total")

    # Mettre à jour
    for key, value in kwargs.items():
        if hasattr(contract, key):
            setattr(contract, key, value)

    db.commit()
    db.refresh(contract)
    return contract


def delete_contract(db: Session, contract_id: int):
    """Supprimer un contrat"""
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    db.delete(contract)
    db.commit()
    return contract


def get_contracts_by_client(db: Session, client_id: int):
    """Obtenir les contrats d'un client"""
    return db.query(Contract).filter(Contract.client_id == client_id).all()


def sign_contract(db: Session, contract_id: int):
    """Signer un contrat"""
    return update_contract(db, contract_id, is_signed=True)


def add_payment(db: Session, contract_id: int, amount: float):
    """Ajouter un paiement"""
    contract = get_contract_by_id(db, contract_id)
    if not contract:
        return None

    if amount <= 0:
        raise ValueError("Le montant doit être positif")

    if amount > contract.remaining_amount:
        raise ValueError("Le paiement dépasse le montant restant")

    new_remaining = contract.remaining_amount - amount
    return update_contract(db, contract_id, remaining_amount=new_remaining)


def get_contract_summary(db: Session):
    """Obtenir un résumé des contrats"""
    total = db.query(func.count(Contract.id)).scalar() or 0
    signed = db.query(func.count(Contract.id)).filter(Contract.is_signed).scalar() or 0
    total_amount = db.query(func.coalesce(func.sum(Contract.total_amount), 0)).scalar() or 0
    remaining = db.query(func.coalesce(func.sum(Contract.remaining_amount), 0)).scalar() or 0

    return {
        'total': total,
        'signed': signed,
        'unsigned': total - signed,
        'total_amount': float(total_amount),
        'remaining_amount': float(remaining),
        'paid_amount': float(total_amount - remaining)
    }


def get_unsigned_contracts(db: Session):
    """Obtenir tous les contrats non signés"""
    return db.query(Contract).filter(Contract.is_signed.is_(False)).all()


def get_unpaid_contracts(db: Session):
    """Obtenir tous les contrats non entièrement payés"""
    return db.query(Contract).filter(Contract.remaining_amount > 0).all()


def get_contracts_by_commercial(db: Session, commercial_id: int):
    """Obtenir tous les contrats d'un commercial"""
    return db.query(Contract).filter(Contract.commercial_id == commercial_id).all()


def search_contracts(db: Session, client_name: str = None, min_amount: float = None,
                     max_amount: float = None, signed: bool = None):
    """Recherche avancée de contrats"""
    query = db.query(Contract).join(Client)

    if client_name:
        query = query.filter(Client.full_name.ilike(f"%{client_name}%"))

    if min_amount is not None:
        query = query.filter(Contract.total_amount >= min_amount)

    if max_amount is not None:
        query = query.filter(Contract.total_amount <= max_amount)

    if signed is not None:
        query = query.filter(Contract.is_signed == signed)

    return query.order_by(Contract.creation_date.desc()).all()


def get_signed_contracts_by_client(db: Session, client_id: int):
    """Récupérer les contrats signés pour un client donné."""
    return (
        db.query(Contract)
        .filter(
                Contract.client_id == client_id,
                Contract.is_signed   # contrats signés uniquement
        )
        .all()
    )
