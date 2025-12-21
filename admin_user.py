# Exécuter ce script
from app.database.database import SessionLocal
from app.crud import crud_users

db = SessionLocal()
try:
    crud_users.create_user(
        db=db,
        full_name="Admin User",
        email="admin@epicevents.com",
        employee_id="ADM001",
        password="admin123",
        department="MANAGEMENT"
    )
    db.commit()
    print("✅ Admin créé")
except Exception as e:
    print(f"❌ Erreur: {e}")
finally:
    db.close()