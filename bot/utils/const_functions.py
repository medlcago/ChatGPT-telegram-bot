import logging
from datetime import datetime

import pytz
from aiogram.utils.deep_linking import decode_payload


def deeplink_decode(payload: str) -> int | None:
    if payload is None:
        return
    try:
        decoded_bytes = int(decode_payload(payload))
        return decoded_bytes
    except Exception as e:
        logging.error(f"Decode payload error: {e}")


def is_number(string: str | int) -> int:
    try:
        if isinstance(string, int):
            return string
        cleaned_string = int(string.replace(" ", "").replace("\xa0", "").replace(",", ""))
        return cleaned_string
    except ValueError:
        return False
    except Exception as e:
        logging.error(e)
        return False


def localize_time(time_string: str | None, date_format: str = '%Y-%m-%d %H:%M:%S') -> datetime | None:
    if time_string:
        moscow_tz = pytz.timezone('Europe/Moscow')
        last_command_time = datetime.strptime(time_string, date_format)
        return moscow_tz.localize(last_command_time)
