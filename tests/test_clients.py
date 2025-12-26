# tests/test_clients.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.crud import crud_clients, crud_users
from app.models.users import Department

TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_create_client(db):
    """Création d'un client associé à un commercial"""
    user = crud_users.create_user(
        db, "Commercial", "sales@test.com", "S001", "pass", "SALES"
    )

    client = crud_clients.create_client(
        db=db,
        full_name="Client Test",
        email="client@test.com",
        phone="+33123456789",
        company_name="Test Corp",
        commercial_id=user.id,
    )

    assert client.id is not None
    assert client.full_name == "Client Test"
    assert client.commercial_id == user.id


def test_update_client(db):
    """Mise à jour d'un client"""
    user = crud_users.create_user(
        db, "Commercial", "sales@test.com", "S001", "pass", "SALES"
    )
    client = crud_clients.create_client(
        db, "Client Test", "client@test.com", "+33123456789", "Test Corp", user.id
    )

    updated = crud_clients.update_client(
        db, client.id, full_name="Client Modifié", email="new@test.com"
    )

    assert updated.full_name == "Client Modifié"
    assert updated.email == "new@test.com"
