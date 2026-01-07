import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.crud.crud_users import create_user
from app.crud.crud_clients import create_client
from app.crud import add_payment, create_contract, sign_contract

TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    yield db
    db.close()
    Base.metadata.drop_all(bind=engine)


def _create_user_and_client(db):
    user = create_user(db, "Commercial", "sales@test.com", "S001", "pass", "SALES")
    client = create_client(db, "Client Test", "client@test.com", "+33123456789", "Test Corp", user.id)
    return user, client


def test_create_contract(db):
    user, client = _create_user_and_client(db)
    contract = create_contract(db, 1000.0, 1000.0, False, client.id, user.id)  # ajoute user_id
    assert contract.id is not None
    assert contract.total_amount == 1000.0


def test_sign_contract(db):
    user, client = _create_user_and_client(db)
    contract = create_contract(db, 1000.0, 1000.0, False, client.id, user.id)
    signed = sign_contract(db, contract.id)
    assert signed.is_signed is True


def test_add_payment(db):
    user, client = _create_user_and_client(db)
    contract = create_contract(db, 1000.0, 1000.0, False, client.id, user.id)
    updated = add_payment(db, contract.id, 200.0)
    assert updated.remaining_amount == 800.0


def test_add_payment_cannot_go_negative(db):
    user, client = _create_user_and_client(db)
    contract = create_contract(db, 1000.0, 1000.0, False, client.id, user.id)
    with pytest.raises(ValueError, match="paiement dépasse"):
        add_payment(db, contract.id, 2000.0)
