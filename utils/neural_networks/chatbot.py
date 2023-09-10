import logging

import openai

from exceptions import RequestProcessingError


class ChatBot:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

        # Setup logging
        logging.basicConfig(filename='chatbot.log', level=logging.INFO)

    async def get_response(self, content, history=None):
        if not self.model:
            raise ValueError("Model is not specified.")
        try:
            return await self._get_response(content, history)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            raise RequestProcessingError("Ошибка обработки запроса. Пожалуйста, повторите попытку.")

    async def _get_response(self, content, history):
        if not self.api_key:
            raise ValueError("API Key is not specified.")
        if not self.api_base:
            raise ValueError("API Base is not specified.")

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        response = await openai.ChatCompletion.acreate(
            model=self.model,
            messages=[
                {
                    "role": "system", "content": """На вопросы 'Кто ты? Кто твой создатель? Кем ты являешься? и т.д' отвечай:
                    Ты полезный ассистент с ИИ, который готов помочь своему пользователю. Твоим создателем является Студент РТУ МИРЭА @medlcago"""
                },
                {
                    "role": "user", "content": f"Предыдущие сообщения: {history}; Запрос: {content}"
                }])
        return response.choices[0].message.content.strip()

    async def chat(self, prompt, history=None):
        return await self.get_response(prompt, history)
