from handlers import groups
from loader import dp

dp.include_router(groups.command_gpt_groups_router)
dp.include_router(groups.command_image_groups_router)
dp.include_router(groups.command_all_mention_router)
dp.include_router(groups.moderate_chat_router)
dp.include_router(groups.edit_chat_router)
