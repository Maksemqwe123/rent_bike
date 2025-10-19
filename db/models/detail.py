from sqlalchemy import Column, String, Float, DateTime, UUID, Boolean, Enum
from config import Base

from enum import Enum as PyEnum
import uuid


class Type(PyEnum):
    TIRE = "tire"
    BRAKE = "brake"
    SHIFT = "shift"
    CHAIN = "chain"
    SPROCKET = "sprocket"
    CRANK = "crank"
    PEDAL = "pedal"
    FRAME = "frame"
    OTHER = "other"


class Detail(Base):
    __tablename__ = "detail"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) # Уже говорил в bicycle.py
    brand = Column(String(50), nullable=False)
    type = Column(Enum(Type), nullable=False)
    name = Column(String(50), nullable=False)
    price = Column(Float, nullable=False) # цена может быть типа Float
    in_stock = Column(Boolean, nullable=False, default=True)
    created = Column(DateTime, nullable=False) # Дата и время когда деталь была добавлена
    updated = Column(DateTime, nullable=False) # Дата и время когда в деталь что то поменяли
