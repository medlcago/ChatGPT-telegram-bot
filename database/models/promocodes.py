from dataclasses import dataclass

from sqlalchemy import Column, String, MetaData
from sqlalchemy.dialects.mysql import TINYINT, BIGINT
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


@dataclass
class Promocode(Base):
    __tablename__ = 'promocodes'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    promocode: str = Column(String(255), unique=True)
    activations_count: int = Column(TINYINT(unsigned=True), default=1)
    individual_activations_count: int = Column(TINYINT(unsigned=True), default=0)
