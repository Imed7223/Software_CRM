import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base


load_dotenv()

# Récupérer l'URL depuis .env
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL non défini dans le fichier .env")

# Désactiver les logs SQLAlchemy
logging.getLogger('sqlalchemy.engine').setLevel(logging.ERROR)

# Créer l'engine
engine = create_engine(
    DATABASE_URL,
    echo=False,       # Désactive l’affichage de toutes les requêtes SQL dans la console
    pool_pre_ping=True,
    pool_recycle=3600
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

    Base.metadata.create_all(bind=engine)
    print("✅ Tables créées avec succès !")


def get_db():
    """Fournir une session de base de données"""
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
