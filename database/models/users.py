from dataclasses import dataclass

from sqlalchemy import Column, String, Text, BOOLEAN
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT

from data.config import load_config
from settings.database import Base

config = load_config()
default_model = config.models.default_model


@dataclass
class User(Base):
    __tablename__ = 'users'

    id: int = Column(BIGINT(unsigned=True), primary_key=True)
    user_id: int = Column(BIGINT(unsigned=True), unique=True)
    fullname: str = Column(Text)
    is_blocked: bool = Column(BOOLEAN, default=False)
    is_admin: bool = Column(BOOLEAN, default=False)
    command_count: int = Column(SMALLINT(unsigned=True), default=0)
    last_command_time: str = Column(Text)
    is_subscriber: bool = Column(BOOLEAN, default=False)
    chat_type: str = Column(String(255), nullable=False, default=default_model)
