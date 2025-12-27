from sqlalchemy import Column, Integer, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.database.database import Base


class Contract(Base):
    __tablename__ = "contracts"

    id = Column(Integer, primary_key=True)
    total_amount = Column(Float, nullable=False)
    remaining_amount = Column(Float, nullable=False)
    creation_date = Column(DateTime, default=func.now())
    is_signed = Column(Boolean, default=False)

    # FK
    client_id = Column(
        Integer,
        ForeignKey("clients.id", ondelete="CASCADE"),
        nullable=False
    )
    commercial_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Relations
    client = relationship("Client", back_populates="contracts")
    commercial = relationship("User", back_populates="contracts")
    events = relationship("Event", back_populates="contract", cascade="all, delete-orphan")

    def __repr__(self):
        signed = "✓" if self.is_signed else "✗"
        return f"<Contract {self.id} - Client {self.client_id}, amount={self.total_amount}, signed={signed})>"
