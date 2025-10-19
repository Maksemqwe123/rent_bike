from sqlalchemy import Column, Float, String, DateTime, UUID, Enum
from config import Base

from enum import Enum as PyEnum
import uuid


class BicycleType(PyEnum):
    MOUNTAIN = "mountain"
    CITY = "city"
    ROAD = "road"
    ELECTRIC = "electric"


class Status(PyEnum):
    AVAILABLE = "available"
    RENTED = "rented"
    MAINTENANCE = "maintenance"
    BROKEN = "broken"
    NOT_AVAILABLE = "not_available"


class Bicycle(Base):
    __tablename__ = "bicycle"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) # Много плюсов от UUID, чем от Integer. Начиная с хэширования, уникальности и т.д.
    brand = Column(String(50), nullable=False)
    type = Column(Enum(BicycleType), nullable=False) # Тип велосипеда, чтобы можно было понять, какой велосипед можно арендовать по типу
    status = Column(Enum(Status), nullable=False) # Статус велосипеда, чтобы понять какой велосипед доступен для аренды
    rent_price = Column(Float, nullable=False)
    created = Column(DateTime, nullable=False) # Дата и время когда велик был добавлен
    updated = Column(DateTime, nullable=False) # Дата и время когда велик был последний раз обновлен
