import logging

from aiogram.utils.deep_linking import decode_payload


def payload_decode(payload):
    if payload is None:
        return
    try:
        decoded_bytes = decode_payload(payload)
        return decoded_bytes
    except Exception as e:
        logging.error(f"Decode payload error: {e}")
