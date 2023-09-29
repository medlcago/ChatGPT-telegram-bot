import logging
from datetime import datetime
from typing import Optional, Sequence, Union

import pytz
from sqlalchemy import update, select, delete, func
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, Member, Promocode, UserDialogues


class Database:
    def __init__(self, session: AsyncSession):
        self.__session = session

    @property
    def session(self):
        """
        Returns the database session.
        """
        return self.__session

    async def add_user(self, user_id: int, fullname: str, referrer: Union[int, None] = None) -> None:
        """
        Adds a new user to the database.
        """
        try:
            user = User(user_id=user_id, fullname=fullname, referrer=referrer)
            self.session.add(user)
            await self.session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def update_admin_rights_status(self, user_id: int, is_admin: bool) -> Optional[bool]:
        """
        Updates the admin rights status of a user in the database.
        """
        try:
            await self.session.execute(update(User).filter_by(user_id=user_id).values(is_admin=is_admin))
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_user(self, user_id: int) -> Optional[User]:
        """
        Checks if a user exists in the database and return their data as a User object.
        """
        try:
            user = await self.session.scalar(select(User).filter_by(user_id=user_id))
            return user
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_all_users(self) -> Optional[Sequence[User]]:
        """
        Retrieves all users from the database and return them as a generator of User objects.
        """
        try:
            users = (await self.session.scalars(select(User))).all()
            return users
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def update_user_block_status(self, user_id: int, is_blocked: bool) -> Optional[bool]:
        """
        Updates the user's block status in the database.
        """
        try:
            await self.session.execute(update(User).filter_by(user_id=user_id).values(is_blocked=is_blocked))
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def check_user_block_status(self, user_id: int) -> Optional[bool]:
        """
        Checks the user's lockout status
        """
        try:
            is_blocked = await self.session.scalar(select(User.is_blocked).filter_by(user_id=user_id))
            return is_blocked
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_all_blocked(self) -> Optional[Sequence[User]]:
        """
        Retrieves all blocked users from the database and returns them as a generator of User objects.
        """
        try:
            blocked_users = (await self.session.scalars(select(User).filter_by(is_blocked=1))).all()
            return blocked_users
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_admins(self) -> Optional[Sequence[User]]:
        """
        Retrieves all admins from the database and return them as a generator of User objects.
        """
        try:
            admins = (await self.session.scalars(select(User).filter_by(is_admin=1))).all()
            return admins
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def check_admin_permissions(self, user_id: int) -> Optional[bool]:
        """
        Checks if the user has administrator rights.
        """
        try:
            is_admin = await self.session.scalar(select(User.is_admin).filter_by(user_id=user_id))
            return is_admin
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_user_command_count(self, user_id: int) -> Optional[int]:
        """
        Retrieves the command count for a specific user in the database.
        """
        try:
            command_count = await self.session.scalar(select(User.command_count).filter_by(user_id=user_id))
            return command_count
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_user_last_command_time(self, user_id: int) -> Optional[datetime]:
        """
        Retrieves the last command time for a specific user in the database.
        """
        try:
            last_command_time = await self.session.scalar(select(User.last_command_time).filter_by(user_id=user_id))
            if last_command_time:
                date_format = '%Y-%m-%d %H:%M:%S'
                moscow_tz = pytz.timezone('Europe/Moscow')
                last_command_time = datetime.strptime(last_command_time, date_format)
                return moscow_tz.localize(last_command_time)
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def reset_user_command_count(self, user_id: int) -> None:
        """
        Resets the command count for a specific user in the database.
        """
        try:
            await self.session.execute(update(User).filter_by(user_id=user_id).values(command_count=0))
            await self.session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def increment_user_command_count(self, user_id: int) -> None:
        """
        Increments the command count for a user in the database.
        """
        try:
            await self.session.execute(
                update(User).filter_by(user_id=user_id).values(command_count=User.command_count + 1))
            await self.session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def update_user_last_command_time(self, user_id: int, time: str) -> None:
        """
        Updates the last command time for a user in the database.
        """
        try:
            await self.session.execute(update(User).filter_by(user_id=user_id).values(last_command_time=time))
            await self.session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_members(self) -> Optional[Sequence[Member]]:
        """
        Gets all members from members table.
        """
        try:
            members = await self.session.scalars(select(Member))
            return members.all()
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_user_chat_type(self, user_id: int) -> Optional[str]:
        """
        Gets user's chat type by its user id.
        """
        try:
            chat_type = await self.session.scalar(select(User.chat_type).filter_by(user_id=user_id))
            return chat_type
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def update_user_chat_type(self, user_id: int, chat_type: str) -> Optional[str]:
        """
        Updates the chat type associated with a given user ID in the database.
        """
        try:
            await self.session.execute(update(User).filter_by(user_id=user_id).values(chat_type=chat_type))
            await self.session.commit()
            return chat_type
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def check_user_subscription_status(self, user_id: int) -> Optional[bool]:
        """
        Check if the user with the given user ID is a subscriber.
        """
        try:
            is_subscriber = await self.session.scalar(select(User.is_subscriber).filter_by(user_id=user_id))
            return is_subscriber
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def update_user_subscription_status(self, user_id: int, is_subscriber: bool) -> Optional[bool]:
        """
        Updates the user's subscription status in the database.
        """
        try:
            await self.session.execute(update(User).filter_by(user_id=user_id).values(is_subscriber=is_subscriber))
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_user_limit(self, user_id: int) -> Optional[int]:
        """
        Gets the user's request limit.
        """
        try:
            request_limit = await self.session.scalar(select(User.limit).filter_by(user_id=user_id))
            return request_limit
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def check_promocode(self, promocode: str) -> Optional[bool]:
        """
        Checks the promo code for validity and increases the number of its activations.
        """
        try:
            is_valid_promo = await self.session.scalar(select(Promocode).filter_by(promocode=promocode))
            if is_valid_promo and is_valid_promo.individual_activations_count < is_valid_promo.activations_count:
                is_valid_promo.individual_activations_count += 1
                await self.session.commit()
                return True
            return False
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def promocode_exists(self, promocode: str) -> Optional[Promocode]:
        """
        Checks if a promo code exists.
        """
        try:
            promocode_exists = await self.session.scalar(select(Promocode).filter_by(promocode=promocode))
            return promocode_exists
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def add_promocode(self, promocode: str, activations_count: int = 1) -> Optional[bool]:
        """
        Adds a new promo code to the database.
        """
        try:
            promocode = Promocode(promocode=promocode, activations_count=activations_count)
            self.session.add(promocode)
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def delete_promocode(self, promocode: str) -> Optional[bool]:
        """
        Deletes the promo code in the database.
        """
        try:
            await self.session.execute(delete(Promocode).filter_by(promocode=promocode))
            await self.session.commit()
            return True
        except Exception as e:
            logging.error(f"Database error: {e}")
            return False

    async def get_user_referral_count(self, user_id: int) -> Optional[int]:
        """
        Gets the number of user referrals.
        """
        try:
            referral_count = await self.session.scalar(
                select(func.count()).where(User.referrer == user_id).select_from(User))
            return referral_count
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def add_message_to_dialog(self, user_id: int, messages: Union[list, tuple]) -> None:
        """
        Adds a new messages to the user's dialog
        """
        try:
            for m in messages:
                message = UserDialogues(user_id=user_id, message=m)
                self.session.add(message)
            await self.session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def get_user_dialog(self, user_id: int, limit: int = 40) -> Optional[Sequence[str]]:
        """
        Gets the user's dialog.
        """
        try:
            dialog = (await self.session.scalars(
                select(UserDialogues.message).filter_by(user_id=user_id).order_by(UserDialogues.id).limit(
                    limit))).all()
            return dialog
        except Exception as e:
            logging.error(f"Database error: {e}")

    async def clear_user_dialog_history(self, user_id: int) -> None:
        """
        Clears the user's dialog history
        """
        try:
            await self.session.execute(delete(UserDialogues).filter_by(user_id=user_id))
            await self.session.commit()
        except Exception as e:
            logging.error(f"Database error: {e}")
