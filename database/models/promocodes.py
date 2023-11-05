from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.dialects.mysql import TINYINT, BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


@dataclass
class Promocode(Base):
    __tablename__ = 'promocodes'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    promocode: Mapped[str] = mapped_column(String(255), unique=True)
    activations_count: Mapped[int] = mapped_column(TINYINT(unsigned=True), default=1)
    individual_activations_count: Mapped[int] = mapped_column(TINYINT(unsigned=True), default=0)
