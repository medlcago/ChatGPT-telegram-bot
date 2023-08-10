from handlers import general
from loader import dp

dp.include_router(general.command_cancel_router)
dp.include_router(general.command_image_router)
