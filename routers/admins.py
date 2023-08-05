from handlers import admins
from loader import dp

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
