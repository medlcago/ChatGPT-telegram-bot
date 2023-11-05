from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


@dataclass
class Model(Base):
    __tablename__ = 'model'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    model_name: Mapped[str] = mapped_column(String(255), unique=True)
    default_limit: Mapped[int] = mapped_column(SMALLINT(unsigned=True))
    premium_limit: Mapped[int] = mapped_column(SMALLINT(unsigned=True))
