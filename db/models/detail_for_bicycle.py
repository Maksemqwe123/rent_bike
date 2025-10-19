from sqlalchemy import Column, Integer, ForeignKey, UUID
from sqlalchemy.orm import relationship as _relationship
from config import Base

import uuid


class DetailForBicycle(Base):
    __tablename__ = "detail_for_bicycle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    bicycle_id = Column(UUID(as_uuid=True), ForeignKey("bicycle.id", ondelete='CASCADE'), nullable=False)
    detail_id = Column(UUID(as_uuid=True), ForeignKey("detail.id", ondelete='CASCADE'), nullable=False)
