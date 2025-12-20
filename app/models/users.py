from sqlalchemy import Column, Integer, String, DateTime, Enum, Text
from sqlalchemy.sql import func
from enum import Enum as PyEnum
from sqlalchemy.orm import relationship
from app.database.database import Base


class Department(PyEnum):
    MANAGEMENT = "MANAGEMENT"
    SALES = "SALES"
    SUPPORT = "SUPPORT"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    employee_id = Column(String, unique=True, nullable=False)
    full_name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    department = Column(Enum(Department), nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)

    # Relations
    clients = relationship("Client", back_populates="commercial_contact")
    contracts = relationship("Contract", back_populates="commercial")
    supported_events = relationship("Event", back_populates="support_contact")

    def __repr__(self):
        return f"<User {self.employee_id}:  name='{self.full_name}', department={self.department})>"
