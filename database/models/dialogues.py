from dataclasses import dataclass

from sqlalchemy import Column, Text, MetaData
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


@dataclass
class UserDialogues(Base):
    __tablename__ = 'user_dialogues'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: int = Column(BIGINT(unsigned=True))
    message: str = Column(Text)
