import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.utils.auth import authenticate_user, verify_password
from app.crud import get_support_users, create_user, get_sales_users


TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope="function")
def db():
    """Fixture DB anti-blocage"""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
        engine.dispose()  # clé !
        Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    user = create_user(db, "Test User", "test@example.com", "TEST001", "password123", "SALES")
    assert user.id is not None
    assert user.full_name == "Test User"
    assert verify_password(user.hashed_password, "password123")


def test_authenticate_user(db):
    create_user(db, "Test User", "test@example.com", "TEST001", "password123", "SALES")
    user = authenticate_user(db, "test@example.com", "password123")
    assert user is not None
    assert user.email == "test@example.com"

    user = authenticate_user(db, "test@example.com", "wrong")
    assert user is None


def test_get_users_by_department(db):
    create_user(db, "Sales 1", "sales1@test.com", "S001", "pass", "SALES")
    create_user(db, "Sales 2", "sales2@test.com", "S002", "pass", "SALES")
    create_user(db, "Support 1", "support1@test.com", "SP001", "pass", "SUPPORT")

    sales_users = get_sales_users(db)
    assert len(sales_users) == 2

    support_users = get_support_users(db)
    assert len(support_users) == 1


def test_create_user_duplicate_email(db):
    create_user(db, "User1", "dup@example.com", "EMP001", "password123", "SALES")
    with pytest.raises(ValueError):
        create_user(db, "User2", "dup@example.com", "EMP002", "password123", "SALES")
