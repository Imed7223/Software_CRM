# tests/tests_unitaires/test_audit.py
from app.models.audit import AuditLog


def test_log_audit_creates_entry(db):
    log = AuditLog(
        user_id=1,
        username="Test User",
        action="LOGIN",
        entity_type="USER",
        entity_id=1,
        details="Test login",
        ip_address="127.0.0.1",
    )

    db.add(log)
    db.commit()
    db.refresh(log)

    all_logs = db.query(AuditLog).all()
    assert len(all_logs) == 1
    assert all_logs[0].action == "LOGIN"
    assert all_logs[0].username == "Test User"
