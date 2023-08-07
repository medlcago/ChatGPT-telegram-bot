import logging
from datetime import datetime

import pytz
from sqlalchemy import update, select
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from data.config import connection_db_string
from .models import User, Member


class Database:
    def __init__(self):
        self._engine = create_async_engine(url=connection_db_string)

    async def get_session(self):
        """
        Returns the database session.
        """
        session = async_sessionmaker(bind=self._engine, expire_on_commit=False, autoflush=False)
        return session()

    async def add_user(self, user_id, fullname):
        """
        Adds a new user to the database.
        """
        try:
            session = await self.get_session()
            user = User(user_id=user_id, fullname=fullname)
            session.add(user)
            await session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def add_or_remove_admin(self, user_id, is_admin):
        """
        Grants or removes administrative rights to the user with the given user ID.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(is_admin=is_admin))
            await session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def user_exists(self, user_id):
        """
        Checks if a user exists in the database and return their data as a User object.
        """
        try:
            session = await self.get_session()
            user = await session.scalar(select(User).filter_by(user_id=user_id))
            if user:
                return user
            return False
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_all_users(self):
        """
        Retrieves all users from the database and return them as a generator of User objects.
        """
        try:
            session = await self.get_session()
            users = (await session.scalars(select(User))).all()
            return users
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def block_or_unblock_user(self, user_id, is_blocked):
        """
        Updates the user's lock status in the database.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(is_blocked=is_blocked))
            await session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def check_user_blocked(self, user_id):
        """
        Checks the user's lockout status
        """
        try:
            session = await self.get_session()
            is_blocked = await session.scalar(select(User.is_blocked).filter_by(user_id=user_id))
            return is_blocked
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_all_blocked(self):
        """
        Retrieves all blocked users from the database and returns them as a generator of User objects.
        """
        try:
            session = await self.get_session()
            blocked_users = (await session.scalars(select(User).filter_by(is_blocked=1))).all()
            return blocked_users
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_admins(self):
        """
        Retrieves all admins from the database and return them as a generator of User objects.
        """
        try:
            session = await self.get_session()
            admins = (await session.scalars(select(User).filter_by(is_admin=1))).all()
            return admins
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def check_admin_permissions(self, user_id):
        """
        Checks if the user has administrator rights.
        """
        try:
            session = await self.get_session()
            is_admin = await session.scalar(select(User.is_admin).filter_by(user_id=user_id))
            return is_admin
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_command_count(self, user_id):
        """
        Retrieves the command count for a specific user in the database.
        """
        try:
            session = await self.get_session()
            command_count = await session.scalar(select(User.command_count).filter_by(user_id=user_id))
            return command_count
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_last_command_time(self, user_id):
        """
        Retrieves the last command time for a specific user in the database.
        """
        try:
            session = await self.get_session()
            last_command_time = await session.scalar(select(User.last_command_time).filter_by(user_id=user_id))
            if last_command_time:
                date_format = '%Y-%m-%d %H:%M:%S'
                moscow_tz = pytz.timezone('Europe/Moscow')
                last_command_time = datetime.strptime(last_command_time, date_format)
                return moscow_tz.localize(last_command_time)
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def reset_command_count(self, user_id):
        """
        Resets the command count for a specific user in the database.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(command_count=0))
            await session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def increment_command_count(self, user_id):
        """
        Increments the command count for a user in the database.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(command_count=User.command_count + 1))
            await session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def update_last_command_time(self, user_id, time):
        """
        Updates the last command time for a user in the database.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(last_command_time=time))
            await session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_members(self):
        """
        Gets all members from members table.
        """
        try:
            session = await self.get_session()
            members = await session.scalars(select(Member))
            return members.all()
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def get_chat_type(self, user_id):
        """
        Gets user's chat type by its user id.
        """
        try:
            session = await self.get_session()
            chat_type = await session.scalar(select(User.chat_type).filter_by(user_id=user_id))
            return chat_type
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def switch_chat_type(self, user_id, chat_type):
        """
        Updates the chat type associated with a given user ID in the database.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(chat_type=chat_type))
            await session.commit()
            return chat_type
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def check_user_subscription(self, user_id):
        """
        Check if the user with the given user ID is a subscriber.
        """
        try:
            session = await self.get_session()
            is_subscriber = await session.scalar(select(User.is_subscriber).filter_by(user_id=user_id))
            return is_subscriber
        except Exception as e:
            logging.error(f"Database error: {e}")
        finally:
            await session.close()

    async def grant_or_remove_subscription(self, user_id, is_subscriber):
        """
        Grants or removes a subscription to the user with the given user ID.
        """
        try:
            session = await self.get_session()
            await session.execute(update(User).filter_by(user_id=user_id).values(is_subscriber=is_subscriber))
            await session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")
            return False
        finally:
            await session.close()
