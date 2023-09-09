from dataclasses import dataclass

from sqlalchemy import Column, String, Text, BOOLEAN
from sqlalchemy import MetaData
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from sqlalchemy.orm import declarative_base

metadata = MetaData()

Base = declarative_base(metadata=metadata)


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
    limit: int = Column(SMALLINT(unsigned=True), nullable=False, default=20)


update_limit_trigger = """
CREATE TRIGGER IF NOT EXISTS update_limit_trigger
BEFORE UPDATE ON users
FOR EACH ROW
BEGIN
    IF NEW.is_subscriber = 1 AND OLD.is_subscriber = 0 THEN
        SET NEW.`limit` = OLD.`limit` * 2;
    ELSEIF NEW.is_subscriber = 0 AND OLD.is_subscriber = 1 THEN
        IF OLD.`limit` / 2 < 20 THEN
            SET NEW.`limit` = 20;
        ELSE
            SET NEW.`limit` = OLD.`limit` / 2;
        END IF;
    END IF;
END;"""
