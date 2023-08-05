from loader import dp
from handlers import users

dp.include_router(users.command_start_help_router)
dp.include_router(users.command_profile_router)
dp.include_router(users.command_image_users_router)
dp.include_router(users.command_limits_router)
dp.include_router(users.command_models_router)
dp.include_router(users.handle_chat_router)
