from sqlalchemy import Column, String, Float, DateTime, UUID
from config import Base

import uuid


class Staff(Base):
    __tablename__ = "staff"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) # Уже говорил в bicycle.py
    name = Column(String(50), nullable=False) # Говорил в client.py
    country = Column(String(50), nullable=False) # Cильно мало данных о сотруднике добавил несколько полей, пометил +
    city = Column(String(50), nullable=False) # +
    address = Column(String(50), nullable=False) # +
    email = Column(String(50), unique=True, nullable=True) # +
    passport = Column(String(50), unique=True, nullable=False) # Говорил в client.py
    phone = Column(String(50), unique=True, nullable=False) # +
    salary = Column(Float, nullable=False) # Зарплата сотрудника
    created = Column(DateTime, nullable=False) # Дата и время когда сотрудник был добавлен
    updated = Column(DateTime, nullable=False) # Дата и время когда сотруднику что то поменяли
