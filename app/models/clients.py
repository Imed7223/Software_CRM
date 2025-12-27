from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True)
    full_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    phone = Column(String, nullable=False)
    company_name = Column(String, nullable=False)
    created_date = Column(DateTime, default=func.now())
    last_contact = Column(DateTime, default=func.now(), nullable=False)
    # FK
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relations
    commercial_contact = relationship("User", back_populates="clients")
    contracts = relationship(
        "Contract",
        back_populates="client",
        cascade="all, delete-orphan"
    )
    events = relationship(
        "Event",
        back_populates="client",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Client(id={self.id},name='{self.full_name}', company='{self.company_name}')>"
