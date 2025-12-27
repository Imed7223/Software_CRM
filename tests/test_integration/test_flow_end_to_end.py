from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.crud import crud_users, crud_clients, crud_contracts, crud_events

TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def setup_function(_):
    Base.metadata.create_all(bind=engine)


def teardown_function(_):
    Base.metadata.drop_all(bind=engine)


def test_full_sales_support_flow():
    db = TestingSessionLocal()

    # 1. Création users
    sales = crud_users.create_user(
        db, "Sales", "sales@test.com", "S001", "pass", "SALES"
    )
    support = crud_users.create_user(
        db, "Support", "support@test.com", "SP001", "pass", "SUPPORT"
    )

    # 2. Client
    client = crud_clients.create_client(
        db, "Client Test", "client@test.com", "+33123456789", "Test Corp", sales.id
    )

    # 3. Contrat signé
    contract = crud_contracts.create_contract(
        db, 1000.0, 1000.0, True, client.id, sales.id
    )

    # 4. Event
    start = datetime.now()
    end = start + timedelta(hours=4)
    event = crud_events.create_event(
        db, "Event Test", start, end, "City", 100, "Notes", client.id, contract.id, support.id
    )

    assert event.client_id == client.id
    assert event.contract_id == contract.id
    assert event.support_id == support.id

    db.close()
