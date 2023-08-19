import logging

import openai

from data.config import load_config


def image_generator(prompt):
    try:
        config = load_config()
        openai.api_key = config.openai.api_key
        openai.api_base = config.openai.api_base
        response = openai.Image.create(
            model="sdxl",
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        logging.error(f'Error processing request: {e}')
