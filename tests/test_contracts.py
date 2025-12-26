# tests/test_contracts.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.crud import crud_users, crud_clients, crud_contracts

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


def _create_user_and_client(db):
    user = crud_users.create_user(
        db, "Commercial", "sales@test.com", "S001", "pass", "SALES"
    )
    client = crud_clients.create_client(
        db, "Client Test", "client@test.com", "+33123456789", "Test Corp", user.id
    )
    return user, client


def test_create_contract(db):
    user, client = _create_user_and_client(db)

    contract = crud_contracts.create_contract(
        db=db,
        total_amount=1000.0,
        remaining_amount=1000.0,
        is_signed=False,
        client_id=client.id,
        commercial_id=user.id,
    )

    assert contract.id is not None
    assert contract.total_amount == 1000.0
    assert contract.remaining_amount == 1000.0
    assert contract.is_signed is False


def test_sign_contract(db):
    user, client = _create_user_and_client(db)
    contract = crud_contracts.create_contract(
        db, 1000.0, 1000.0, False, client.id, user.id
    )

    signed = crud_contracts.sign_contract(db, contract.id)
    assert signed.is_signed is True


def test_add_payment(db):
    user, client = _create_user_and_client(db)
    contract = crud_contracts.create_contract(
        db, 1000.0, 1000.0, False, client.id, user.id
    )

    updated = crud_contracts.add_payment(db, contract.id, 200.0)
    assert updated.remaining_amount == 800.0
