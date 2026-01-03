import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.crud.crud_users import create_user
from app.crud import create_client, update_client

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


def test_create_client(db):
    user = create_user(db, "Commercial", "sales@test.com", "S001", "pass", "SALES")

    client = create_client(db, "Client Test", "client@test.com", "+33123456789", "Test Corp", user.id)
    assert client.id is not None
    assert client.full_name == "Client Test"
    assert client.commercial_id == user.id


def test_update_client(db):
    user = create_user(db, "Commercial", "sales@test.com", "S001", "pass", "SALES")
    client = create_client(db, "Client Test", "client@test.com", "+33123456789", "Test Corp", user.id)

    updated = update_client(db, client.id, full_name="Client Modifié", email="new@test.com")
    assert updated.full_name == "Client Modifié"
    assert updated.email == "new@test.com"


def test_create_client_without_commercial_fails(db):
    with pytest.raises(ValueError, match="Commercial ID"):
        create_client(db, "Client Sans Com", "noc@test.com", "0612345678", "No Sales Corp", None)  # ✅ OK
