from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


@dataclass
class Model(Base):
    __tablename__ = 'model'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    model_name: str = Column(String(255), unique=True)
    default_limit: int = Column(SMALLINT(unsigned=True), nullable=False)
    premium_limit: int = Column(SMALLINT(unsigned=True), nullable=False)
