from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.crud.crud_users import create_user
from app.crud.crud_clients import create_client
from app.crud.crud_contracts import create_contract
from app.crud.crud_events import create_event

TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


def setup_module():
    Base.metadata.create_all(bind=engine)


def teardown_module():
    Base.metadata.drop_all(bind=engine)


def test_full_sales_support_flow():
    db = TestingSessionLocal()

    sales = create_user(db, "Sales", "sales@test.com", "S001", "pass", "SALES")
    db.commit()
    support = create_user(db, "Support", "support@test.com", "SP001", "pass", "SUPPORT")
    db.commit()

    client = create_client(db, "Client Test", "client@test.com", "+33123456789", "Test Corp", sales.id)
    db.commit()

    contract = create_contract(db, 1000.0, 1000.0, True, client.id, sales.id)
    db.commit()

    start = datetime.now()
    end = start + timedelta(hours=4)
    event = create_event(db, "Event Test", start, end, "City", 100, "Notes",
                         client.id, contract.id, support.id)
    db.commit()

    assert event.client_id == client.id
    assert event.contract_id == contract.id
    assert event.support_id == support.id

    db.close()
