from dataclasses import dataclass

from sqlalchemy import Column, BigInteger, Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class Member(Base):
    __tablename__ = 'members'

    id: int = Column(BigInteger, primary_key=True, unique=True, nullable=False)
    user_id: int = Column(BigInteger)
    username: str = Column(Text)
    nickname: str = Column(Text)
