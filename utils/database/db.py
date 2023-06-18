import aiomysql
import pytz
from dataclasses import dataclass
from datetime import datetime

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
                await cursor.execute("INSERT INTO users (user_id, fullname) VALUES (%s, %s)", (user_id, fullname))
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
                await cursor.execute("UPDATE users SET is_admin = (%s) WHERE user_id = (%s)", (is_admin, user_id))
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
                await cursor.execute("SELECT * FROM users WHERE user_id = (%s)", (user_id,))
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
                await cursor.execute("SELECT * FROM users")
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
                await cursor.execute("UPDATE users SET is_blocked = (%s) WHERE user_id = (%s)", (is_blocked, user_id))
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
                await cursor.execute("SELECT * FROM users WHERE is_admin = (%s)", (1,))
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
                await cursor.execute("SELECT gpt4_command_count FROM users WHERE user_id = (%s)", (user_id,))
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
                await cursor.execute("SELECT last_gpt4_command_time FROM users WHERE user_id = (%s)", (user_id,))
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
                await cursor.execute("UPDATE users SET gpt4_command_count = (%s) WHERE user_id = (%s)", (0, user_id))
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
                await cursor.execute(
                    "UPDATE users SET gpt4_command_count = gpt4_command_count + 1 WHERE user_id = (%s)", (user_id,))
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
                await cursor.execute("UPDATE users SET last_gpt4_command_time = (%s) WHERE user_id = (%s)", (time, user_id))
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
                await cursor.execute("SELECT * FROM members")
                members = await cursor.fetchall()
                connection.close()
                return members
        except Exception as e:
            print(e)

    async def get_chat_type(self, user_id):
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                await cursor.execute("SELECT chat_type FROM users WHERE user_id = %s", (user_id,))
                result = await cursor.fetchone()
            connection.close()
            return 'gpt-3' if result[0] == 1 else 'gpt-4' if result[0] == 2 else 'bing'
        except Exception as e:
            print(e)

    async def switch_chat_type(self, user_id, chat_type):
        try:
            connection = await self._connect_db()
            async with connection.cursor() as cursor:
                await cursor.execute("UPDATE users SET chat_type = %s WHERE user_id = %s", (chat_type, user_id))
                await connection.commit()
            connection.close()
            return 'gpt-3' if chat_type == 1 else 'gpt-4' if chat_type == 2 else 'bing'
        except Exception as e:
            print(e)
