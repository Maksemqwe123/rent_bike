from sqlalchemy import Column, Integer, ForeignKey, Boolean, UUID, DateTime
from sqlalchemy.orm import relationship as _relationship
from config import Base

import uuid


class RentBook(Base):
    __tablename__ = "rent_book"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    time = Column(Integer, nullable=False)
    paid = Column(Boolean, nullable=False)
    bicycle_id = Column(UUID(as_uuid=True), ForeignKey("bicycle.id", ondelete='CASCADE'), nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("client.id", ondelete='CASCADE'), nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete='CASCADE'), nullable=False)
    created = Column(DateTime, nullable=False) # Время когда началась аренда
    updated = Column(DateTime, nullable=False) # Время когда что то поменяли
