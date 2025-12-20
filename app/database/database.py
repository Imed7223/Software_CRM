import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config

# Désactiver les logs SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# Créer l'engine
engine = create_engine(
    Config.DATABASE_URL,
    echo=False,  # Désactiver l'echo des requêtes
    pool_pre_ping=True,  # Vérifier la connexion avant utilisation
    pool_recycle=3600  # Recycler les connexions toutes les heures
)

# Session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

# Base pour les modèles
Base = declarative_base()

def init_db():
    """Initialiser la base de données (créer les tables)"""
    from app.models import users, clients, contracts, events
    Base.metadata.create_all(bind=engine)

def get_db():
    """Fournir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()