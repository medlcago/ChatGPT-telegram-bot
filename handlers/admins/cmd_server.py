import datetime
import platform

import psutil
from aiogram import types, Router, F
from aiogram.filters.command import Command

from decorators import MessageLogging
from filters import IsAdmin, ChatTypeFilter
from keyboards.inline import btn_back_admin_panel

command_server_router = Router()


async def get_server_system_info():
    delimiter = "-" * 55 + "\n"

    date_info = f'<b>Дата и время:</b> {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}\n'
    os_info = f"<b>Операционная система:</b> {platform.system()} {platform.version()}\n"
    python_version = f"<b>Версия Python:</b> {platform.python_version()}\n"

    cpu_info = f"<b>Процессор:</b> {platform.machine()} {psutil.cpu_count(logical=False)} ядер {psutil.cpu_count(logical=True)} потоков\n"
    memory_info = f"<b>Оперативная память:</b> {round(psutil.virtual_memory().total / (1024 * 1024 * 1024), 2)} ГБ\n"

    cpu_load = f"<b>Загрузка процессора:</b> {psutil.cpu_percent(interval=1)} %\n"
    memory_load = f"<b>Загрузка оперативной памяти:</b> {psutil.virtual_memory().percent} %\n"

    parts = psutil.disk_partitions()
    disk_information = "<b>Свободное место на дисках (ГБ):</b>\n"
    for part in parts:
        disk_name = part.device
        usage = psutil.disk_usage(part.mountpoint)
        free = round(usage.free / 1024 / 1024 / 1024, 2)
        disk_information += f"*Диск {disk_name} : {free} ГБ\n"

    return (date_info + os_info + python_version) + delimiter + (cpu_info + memory_info) + \
        delimiter + (cpu_load + memory_load) + delimiter + disk_information + delimiter


@command_server_router.message(Command(commands=["server"], prefix="!/"), ChatTypeFilter(is_group=False), IsAdmin())
@MessageLogging
async def command_server(message: types.Message):
    result = await get_server_system_info()
    await message.reply(result)


@command_server_router.callback_query(F.data.in_({"server_info"}), IsAdmin())
@MessageLogging
async def command_server(call: types.CallbackQuery):
    result = await get_server_system_info()
    await call.message.edit_text(result, reply_markup=btn_back_admin_panel)
    await call.answer("Успех!")
