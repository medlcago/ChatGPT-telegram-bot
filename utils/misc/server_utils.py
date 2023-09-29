import datetime
import platform

import psutil


def get_server_system_info():
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
