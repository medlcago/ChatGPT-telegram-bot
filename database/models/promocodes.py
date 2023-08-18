from dataclasses import dataclass

from sqlalchemy import Column, String
from sqlalchemy.dialects.mysql import TINYINT, BIGINT

from settings.database import Base


@dataclass
class Promocode(Base):
    __tablename__ = 'promocodes'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    promocode: str = Column(String(255), unique=True)
    activations_count: int = Column(TINYINT(unsigned=True), default=1)
    individual_activations_count: int = Column(TINYINT(unsigned=True), default=0)
