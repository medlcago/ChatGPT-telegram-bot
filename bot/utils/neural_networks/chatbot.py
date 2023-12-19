import logging

import openai

from bot.exceptions import RequestProcessingError


class ChatBot:
    __slots__ = ("api_key", "api_base", "model")

    def __init__(self, api_key: str, api_base: str, model: str):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

    async def get_response(self, content: str, history: str | None = None) -> str:
        if not self.model:
            raise ValueError("Model is not specified.")
        try:
            return await self._get_response(content, history)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            raise RequestProcessingError("Error processing request. Please, try again.")

    async def _get_response(self, content: str, history: str | None = None) -> str:
        if not self.api_key:
            raise ValueError("API Key is not specified.")
        if not self.api_base:
            raise ValueError("API Base is not specified.")

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        history = history or " "
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {
                    "role": "system", "content": "Ты полезный ассистент с ИИ, который готов помочь своему пользователю."
                },
                {
                    "role": "user", "content": f"Предыдущие сообщения: {history}; Запрос: {content}"
                }],
            timeout=60)
        return response.choices[0].message.content.strip()

    async def chat(self, prompt, history=None) -> str:
        return await self.get_response(prompt, history)
