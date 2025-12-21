import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import Config


load_dotenv()

DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "epicevents_crm")

# Encodage du mot de passe (utile si caractères spéciaux)

DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

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
    print("✅ Tables créées avec succès !")
def get_db():
    """Fournir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()