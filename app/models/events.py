from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.database import Base


class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    location = Column(String, nullable=False)
    attendees = Column(Integer, nullable=False)
    notes = Column(Text)

    # FK
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)
    contract_id = Column(Integer, ForeignKey("contracts.id"), nullable=False)
    support_id = Column(Integer, ForeignKey("users.id"))

    # Relations
    client = relationship("Client", back_populates="events")
    contract = relationship("Contract", back_populates="events")
    support_contact = relationship("User", back_populates="supported_events")

    def __repr__(self):
        return f"<Event(id={self.id}, name='{self.name}', start={self.start_date})>"
