from handlers import users
from loader import dp

dp.include_router(users.command_start_help_router)
dp.include_router(users.command_profile_router)
dp.include_router(users.command_promocode_router)
dp.include_router(users.command_summary_router)
dp.include_router(users.command_limits_router)
dp.include_router(users.command_models_router)
dp.include_router(users.handle_chat_router)
