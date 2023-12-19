import logging

import openai

from bot.exceptions import RequestProcessingError


class ImageGenerator:
    __slots__ = ("api_key", "api_base", "model")

    def __init__(self, api_key: str, api_base: str, model: str):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

    async def get_response(self, content: str):
        if not self.model:
            raise ValueError("Model is not specified.")
        try:
            return await self._get_response(content)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            raise RequestProcessingError("Error processing request. Please, try again.")

    async def _get_response(self, content: str):
        if not self.api_key:
            raise ValueError("API Key is not specified.")
        if not self.api_base:
            raise ValueError("API Base is not specified.")

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        response = await openai.Image.acreate(
            model=self.model,
            prompt=content,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']

    async def generate_image(self, prompt: str):
        return await self.get_response(prompt)
