from dataclasses import dataclass

from sqlalchemy import Column, String, Text, BOOLEAN
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT

from settings.database import Base


@dataclass
class User(Base):
    __tablename__ = 'users'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: int = Column(BIGINT(unsigned=True), unique=True)
    fullname: str = Column(Text)
    referrer: int = Column(BIGINT(unsigned=True))
    is_blocked: bool = Column(BOOLEAN, default=False)
    is_admin: bool = Column(BOOLEAN, default=False)
    is_subscriber: bool = Column(BOOLEAN, default=False)
    last_command_time: str = Column(Text)
    command_count: int = Column(SMALLINT(unsigned=True), default=0)
    chat_type: str = Column(String(255), nullable=False, default="gpt-3.5-turbo")
