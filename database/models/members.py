from dataclasses import dataclass

from sqlalchemy import String
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


@dataclass
class Member(Base):
    __tablename__ = 'members'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), unique=True)
    username: Mapped[str] = mapped_column(String(length=32), unique=True)
    nickname: Mapped[str] = mapped_column(String(length=64))
