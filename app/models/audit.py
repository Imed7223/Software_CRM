"""
Modèle pour le journal d'audit
"""
from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from app.database.database import Base


class AuditLog(Base):
    """Journal d'audit des actions utilisateurs"""
    __tablename__ = "audit_logs"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, server_default=func.now(), nullable=False)
    user_id = Column(Integer, nullable=False)
    username = Column(String(100), nullable=False)
    action = Column(String(100), nullable=False)  # CREATE, UPDATE, DELETE, LOGIN, etc.
    entity_type = Column(String(50))  # USER, CLIENT, CONTRACT, EVENT
    entity_id = Column(Integer)  # ID de l'entité concernée
    details = Column(Text)  # Détails de l'action
    ip_address = Column(String(45))  # Adresse IP

    def __repr__(self):
        return f"<AuditLog(id={self.id}, user={self.username}, action={self.action})>"