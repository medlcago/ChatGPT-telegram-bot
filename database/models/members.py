from dataclasses import dataclass

from sqlalchemy import Column, Text, MetaData
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


@dataclass
class Member(Base):
    __tablename__ = 'members'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: int = Column(BIGINT(unsigned=True), unique=True)
    username: str = Column(Text, unique=True)
    nickname: str = Column(Text)
