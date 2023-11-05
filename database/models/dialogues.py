from dataclasses import dataclass

from sqlalchemy import Text
from sqlalchemy.dialects.mysql import BIGINT
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


@dataclass
class UserDialogues(Base):
    __tablename__ = 'user_dialogues'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT(unsigned=True))
    message: Mapped[str] = mapped_column(Text)
