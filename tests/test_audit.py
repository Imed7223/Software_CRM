import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.database import Base
from app.models.audit import AuditLog

TEST_DATABASE_URL = "postgresql://postgres:Imed7223@localhost:5432/epicevents_test"
engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


def test_log_audit_creates_entry(db):
    log = AuditLog(user_id=1, username="Test User", action="LOGIN",
                   entity_type="USER", entity_id=1, details="Test login",
                   ip_address="127.0.0.1")
    db.add(log)
    db.commit()
    db.refresh(log)

    all_logs = db.query(AuditLog).all()
    assert len(all_logs) == 1
    assert all_logs[0].action == "LOGIN"
