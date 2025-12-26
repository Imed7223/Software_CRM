# tests/test_users.py
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database import Base
from app.models.users import Department
from app.crud import crud_users
from app.utils.auth import verify_password


# Base de données de test Postgres
TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    # Création du schéma avant chaque test
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        # Nettoyage du schéma après chaque test
        Base.metadata.drop_all(bind=engine)


def test_create_user(db):
    """Test création d'utilisateur"""
    user = crud_users.create_user(
        db=db,
        full_name="Test User",
        email="test@example.com",
        employee_id="TEST001",
        password="password123",
        department="SALES",
    )

    assert user.id is not None
    assert user.full_name == "Test User"
    assert user.department == Department.SALES
    assert verify_password(user.hashed_password, "password123")


def test_authenticate_user(db):
    """Test authentification"""
    from app.utils.auth import authenticate_user

    crud_users.create_user(
        db=db,
        full_name="Test User",
        email="test@example.com",
        employee_id="TEST001",
        password="password123",
        department="SALES",
    )

    # Authentification réussie
    user = authenticate_user(db, "test@example.com", "password123")
    assert user is not None
    assert user.email == "test@example.com"

    # Mot de passe incorrect
    user = authenticate_user(db, "test@example.com", "wrongpassword")
    assert user is None

    # Email inconnu
    user = authenticate_user(db, "unknown@example.com", "password123")
    assert user is None


def test_get_users_by_department(db):
    """Test récupération par département"""
    crud_users.create_user(db, "Sales 1", "sales1@test.com", "S001", "pass", "SALES")
    crud_users.create_user(db, "Sales 2", "sales2@test.com", "S002", "pass", "SALES")
    crud_users.create_user(db, "Support 1", "support1@test.com", "SP001", "pass", "SUPPORT")

    sales_users = crud_users.get_sales_users(db)
    assert len(sales_users) == 2
    assert all(u.department == Department.SALES for u in sales_users)

    support_users = crud_users.get_support_users(db)
    assert len(support_users) == 1
    assert support_users[0].department == Department.SUPPORT
