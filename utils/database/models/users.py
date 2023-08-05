from dataclasses import dataclass

from sqlalchemy import Column, Integer, String, Text, BigInteger
from sqlalchemy.orm import declarative_base

from data.config import default_model

Base = declarative_base()


@dataclass
class User(Base):
    __tablename__ = 'users'

    id: int = Column(BigInteger, primary_key=True, unique=True)
    user_id: int = Column(BigInteger, unique=True)
    fullname: str = Column(Text)
    is_blocked: int = Column(Integer, default=0)
    is_admin: int = Column(Integer, default=0)
    command_count: int = Column(Integer, default=0)
    last_command_time: str = Column(Text)
    is_subscriber: int = Column(Integer, default=0)
    chat_type: str = Column(String(255), nullable=False, default=default_model)
