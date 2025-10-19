from sqlalchemy import Column, ForeignKey, UUID, Float, DateTime
from config import Base

import uuid


class ServiceBook(Base):
    __tablename__ = "service_book"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    bicycle_id = Column(UUID(as_uuid=True), ForeignKey("bicycle.id", ondelete='CASCADE'), nullable=False)
    detail_id = Column(UUID(as_uuid=True), ForeignKey("detail.id", ondelete='CASCADE'), nullable=False)
    price = Column(Float, nullable=False)
    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id", ondelete='CASCADE'), nullable=False)
    created = Column(DateTime, nullable=False) # Время когда началось обслуживание
    updated = Column(DateTime, nullable=False) # Время когда что то поменяли
