from loader import dp

from handlers import users
from handlers import groups
from handlers import admins

dp.include_router(users.command_start_help_router)
dp.include_router(users.command_profile_router)
dp.include_router(users.command_image_users_router)
dp.include_router(users.command_limits_router)
dp.include_router(users.command_models_router)

dp.include_router(groups.command_gpt_groups_router)
dp.include_router(groups.command_image_groups_router)
dp.include_router(groups.command_all_mention_router)
dp.include_router(groups.moderate_chat_router)
dp.include_router(groups.edit_chat_router)

dp.include_router(admins.command_admin_router)
dp.include_router(admins.command_send_all_router)
dp.include_router(admins.command_send_message_router)
dp.include_router(admins.command_user_list_router)
dp.include_router(admins.command_admin_list_router)
dp.include_router(admins.command_server_router)
dp.include_router(admins.command_add_admin_router)
dp.include_router(admins.command_remove_admin_router)
dp.include_router(admins.command_grant_sub_router)
dp.include_router(admins.command_remove_sub_router)
dp.include_router(admins.command_statistics_router)

dp.include_router(users.handle_chat_router)
