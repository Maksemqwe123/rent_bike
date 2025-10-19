from sqlalchemy import Column, String, UUID, DateTime
from config import Base

import uuid


class Client(Base):
    __tablename__ = "client"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True) # Уже говорил в bicycle.py
    name = Column(String(50), nullable=False) # Очень маленькое ограничение, ни у всех людей имя будет короче 10 символов
    passport = Column(String(50), unique=True, nullable=False) # Если мы говорим о паспорте, а именно о индентификационном номере, то индентификационном номер у каждого человека уникальный
    phone = Column(String(50), unique=True, nullable=False) # Зачем поле называется phone_number и так понятно, что клиент оставит моб. телефон. Вряд-ли что клиент оставит домашний телефон :) Телефон также у всех уникальный
    country = Column(String(50), nullable=False)
    city = Column(String(50), nullable=False) # Никогда не бывает лишней информацией
    address = Column(String(50), nullable=False) # Никогда не бывает лишней информацией
    email = Column(String(50), unique=True, nullable=True) # Никогда не бывает лишней информацией
    created = Column(DateTime, nullable=False) # Дата и время когда клиент был добавлен
    updated = Column(DateTime, nullable=False) # Дата и время когда клиент был последний раз обновлен

