from dataclasses import dataclass
from datetime import datetime

import aiomysql
import pytz

from data import config


@dataclass(order=True, frozen=True)
class UserData:
    id: int = None
    user_id: int = None
    fullname: str = None
    is_blocked: bool = None
    is_admin: bool = None
    gpt4_command_count: int = None
    last_gpt4_command_time: datetime = None
    chat_type: int = None
    is_subscriber: bool = None


class Database:
    def __init__(self):
        self.__host = config.host
        self.__port = config.port
        self.__user = config.user
        self.__password = config.password
        self.__db = config.db

    async def _connect_db(self):
        """
        Establish a connection to the database with given parameters.
        """
        return await aiomysql.connect(
            host=self.__host,
            port=self.__port,
            user=self.__user,
            password=self.__password,
            db=self.__db
        )

    async def add_user(self, user_id, fullname):
        """
        Add a new user to the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'INSERT INTO users (user_id, fullname) VALUES (%s, %s)'
                params = (user_id, fullname)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    async def add_or_remove_admin(self, user_id, is_admin):
        """
        Update the admin status of a user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET is_admin = (%s) WHERE user_id = (%s)'
                params = (is_admin, user_id)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    async def user_exists(self, user_id):
        """
        Check if a user exists in the database and return their data as a UserData object.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor(aiomysql.cursors.DictCursor) as cursor:
                query = 'SELECT * FROM users WHERE user_id = (%s)'
                params = (user_id,)
                await cursor.execute(query, params)
                user_exists = await cursor.fetchone()
                connection.close()
                if user_exists:
                    return UserData(*user_exists.values())
                return False
        except Exception as e:
            print(e)

    async def get_all_users(self):
        """
        Retrieve all users from the database and return them as a generator of UserData objects.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor(aiomysql.cursors.DictCursor) as cursor:
                query = 'SELECT * FROM users'
                await cursor.execute(query)
                all_users = (UserData(*user.values()) for user in await cursor.fetchall())
                connection.close()
                return all_users
        except Exception as e:
            print(e)

    async def block_or_unblock_user(self, user_id, is_blocked):
        """
        Update the block status of a user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET is_blocked = (%s) WHERE user_id = (%s)'
                params = (is_blocked, user_id)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    async def get_admins(self):
        """
        Retrieve all admins from the database and return them as a generator of UserData objects.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor(aiomysql.cursors.DictCursor) as cursor:
                query = 'SELECT * FROM users WHERE is_admin = (%s)'
                params = (1,)
                await cursor.execute(query, params)
                admins = (UserData(*admin.values()) for admin in await cursor.fetchall())
                connection.close()
                return admins
        except Exception as e:
            print(e)

    async def get_gpt4_command_count(self, user_id):
        """
        Retrieve the GPT-4 command count for a specific user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor(aiomysql.cursors.DictCursor) as cursor:
                query = 'SELECT gpt4_command_count FROM users WHERE user_id = (%s)'
                params = (user_id,)
                await cursor.execute(query, params)
                gpt4_command_count = (await cursor.fetchone())["gpt4_command_count"]
                connection.close()
                return gpt4_command_count
        except Exception as e:
            print(e)

    async def get_last_gpt4_command_time(self, user_id):
        """
        Retrieve the last GPT-4 command time for a specific user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor(aiomysql.cursors.DictCursor) as cursor:
                query = 'SELECT last_gpt4_command_time FROM users WHERE user_id = (%s)'
                params = (user_id,)
                await cursor.execute(query, params)
                last_gpt4_command_time = (await cursor.fetchone())["last_gpt4_command_time"]
                connection.close()
                if last_gpt4_command_time:
                    date_format = '%Y-%m-%d %H:%M:%S'
                    moscow_tz = pytz.timezone('Europe/Moscow')
                    last_gpt4_command_time = datetime.strptime(last_gpt4_command_time, date_format)
                    return moscow_tz.localize(last_gpt4_command_time)
                return None
        except Exception as e:
            print(e)

    async def reset_gpt4_command_count(self, user_id):
        """
        Reset the GPT-4 command count for a specific user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET gpt4_command_count = (%s) WHERE user_id = (%s)'
                params = (0, user_id)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    async def increment_gpt4_command_count(self, user_id):
        """
        Increment the GPT-4 command count for a user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET gpt4_command_count = gpt4_command_count + 1 WHERE user_id = (%s)'
                params = (user_id,)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    async def update_last_gpt4_command_time(self, user_id, time):
        """
        Update the last GPT-4 command time for a user in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET last_gpt4_command_time = (%s) WHERE user_id = (%s)'
                params = (time, user_id)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
        except Exception as e:
            print(e)

    async def get_members(self):
        """
        Retrieve all members from the database and return them as a dict.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor(aiomysql.cursors.DictCursor) as cursor:
                query = 'SELECT * FROM members'
                await cursor.execute(query)
                members = await cursor.fetchall()
                connection.close()
                return members
        except Exception as e:
            print(e)

    async def get_chat_type(self, user_id):
        """
        Fetch the chat type associated with a given user ID from the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'SELECT chat_type FROM users WHERE user_id = %s'
                params = (user_id,)
                await cursor.execute(query, params)
                result = await cursor.fetchone()
            connection.close()
            return config.reverse_chat_type_mapping.get(result[0], 'gpt-3')
        except Exception as e:
            print(e)

    async def switch_chat_type(self, user_id, chat_type):
        """
        Update the chat type associated with a given user ID in the database.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET chat_type = %s WHERE user_id = %s'
                params = (chat_type, user_id)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
            return config.reverse_chat_type_mapping.get(chat_type, 'gpt-3')
        except Exception as e:
            print(e)

    async def check_user_subscription(self, user_id):
        """
        Check if the user with the given user ID is a subscriber or not.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'SELECT is_subscriber FROM users WHERE user_id = %s'
                params = (user_id,)
                await cursor.execute(query, params)
                result = await cursor.fetchone()
            connection.close()
            if result is not None:
                return result[0]
        except Exception as e:
            print(e)

    async def grant_or_remove_subscription(self, user_id, is_subscriber):
        """
        Grant or remove a subscription to the user with the given user ID.
        """
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                query = 'UPDATE users SET is_subscriber = %s WHERE user_id = %s'
                params = (is_subscriber, user_id)
                await cursor.execute(query, params)
                await connection.commit()
            connection.close()
            return True
        except Exception as e:
            print(e)
            return False
