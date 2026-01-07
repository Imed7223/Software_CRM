import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.crud.crud_users import create_user
from app.crud.crud_clients import create_client
from app.crud.crud_contracts import create_contract
from app.crud import create_event, get_events_without_support

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


def _create_user_client_contract(db):
    sales = create_user(db, "Commercial", "sales@test.com", "S001", "pass", "SALES")
    support = create_user(db, "Support", "support@test.com", "SP001", "pass", "SUPPORT")
    client = create_client(db, "Client Test", "client@test.com", "+33123456789", "Test Corp", sales.id)
    contract = create_contract(db, 1000.0, 1000.0, True, client.id, sales.id)
    return sales, support, client, contract


def test_create_event(db):
    sales, support, client, contract = _create_user_client_contract(db)
    start = datetime.now()
    end = start + timedelta(hours=4)
    event = create_event(db, "Test Event", start, end, "Test City", 50, "Notes",
                         client.id, contract.id, support.id)
    assert event.id is not None
    assert event.client_id == client.id


def test_get_events_without_support(db):
    sales, support, client, contract = _create_user_client_contract(db)
    start = datetime.now()
    end = start + timedelta(hours=4)

    create_event(db, "With support", start, end, "City", 50, "", client.id, contract.id, support.id)
    create_event(db, "Without support", start, end, "City", 30, "", client.id, contract.id, None)

    events = get_events_without_support(db)
    assert len(events) == 1
    assert events[0].name == "Without support"


def test_cannot_create_event_if_contract_not_signed(db):
    sales = create_user(db, "Commercial", "sales@test.com", "S001", "pass", "SALES")
    support = create_user(db, "Support", "support@test.com", "SP001", "pass", "SUPPORT")
    client = create_client(db, "Client Test", "client@test.com", "+33123456789", "Test Corp", sales.id)
    contract = create_contract(db, 1000.0, 1000.0, False, client.id, sales.id)  # NON signé

    start = datetime.now()
    end = start + timedelta(hours=4)

    with pytest.raises(ValueError, match="doit être signé"):
        create_event(db, "Event invalid", start, end, "City", 10, "",
                     client.id, contract.id, support.id)


def test_create_event_invalid_dates(db):
    sales, support, client, contract = _create_user_client_contract(db)
    start = datetime.now()
    end = start - timedelta(hours=1)  # fin AVANT début
    with pytest.raises(ValueError, match="date de fin"):
        create_event(db, "Bad dates", start, end, "City", 10, "",
                     client.id, contract.id, support.id)


def test_create_event_negative_attendees(db):
    sales, support, client, contract = _create_user_client_contract(db)
    start = datetime.now()
    end = start + timedelta(hours=1)
    with pytest.raises(ValueError, match="participants ne peut pas"):
        create_event(db, "Bad attendees", start, end, "City", -5, "",
                     client.id, contract.id, support.id)
