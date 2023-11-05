from dataclasses import dataclass

from sqlalchemy import String, Text
from sqlalchemy.dialects.mysql import BIGINT, SMALLINT
from sqlalchemy.orm import Mapped, mapped_column

from database.models import Base


@dataclass
class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(BIGINT(unsigned=True), primary_key=True)
    user_id: Mapped[int] = mapped_column(BIGINT(unsigned=True), unique=True)
    fullname: Mapped[str] = mapped_column(Text)
    referrer: Mapped[int] = mapped_column(BIGINT(unsigned=True))
    is_blocked: Mapped[bool] = mapped_column(default=False)
    is_admin: Mapped[bool] = mapped_column(default=False)
    is_subscriber: Mapped[bool] = mapped_column(default=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    last_command_time: Mapped[str] = mapped_column(Text)
    command_count: Mapped[int] = mapped_column(SMALLINT(unsigned=True), default=0)
    chat_type: Mapped[str] = mapped_column(String(255), default="gpt-3.5-turbo")
    limit: Mapped[int] = mapped_column(SMALLINT(unsigned=True), default=20)


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
