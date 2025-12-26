# tests/test_events.py
import pytest
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.crud import crud_users, crud_clients, crud_contracts, crud_events

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


def _create_user_client_contract(db):
    sales = crud_users.create_user(
        db, "Commercial", "sales@test.com", "S001", "pass", "SALES"
    )
    support = crud_users.create_user(
        db, "Support", "support@test.com", "SP001", "pass", "SUPPORT"
    )
    client = crud_clients.create_client(
        db, "Client Test", "client@test.com", "+33123456789", "Test Corp", sales.id
    )
    contract = crud_contracts.create_contract(
        db, 1000.0, 1000.0, True, client.id, sales.id
    )
    return sales, support, client, contract


def test_create_event(db):
    sales, support, client, contract = _create_user_client_contract(db)

    start = datetime.now()
    end = start + timedelta(hours=4)

    event = crud_events.create_event(
        db=db,
        name="Test Event",
        start_date=start,
        end_date=end,
        location="Test City",
        attendees=50,
        notes="Notes",
        client_id=client.id,
        contract_id=contract.id,
        support_id=support.id,
    )

    assert event.id is not None
    assert event.client_id == client.id
    assert event.contract_id == contract.id
    assert event.support_id == support.id


def test_get_events_without_support(db):
    sales, support, client, contract = _create_user_client_contract(db)

    start = datetime.now()
    end = start + timedelta(hours=4)

    crud_events.create_event(
        db, "With support", start, end, "City", 50, "", client.id, contract.id, support.id
    )
    crud_events.create_event(
        db, "Without support", start, end, "City", 30, "", client.id, contract.id, None
    )

    events = crud_events.get_events_without_support(db)
    assert len(events) == 1
    assert events[0].name == "Without support"
