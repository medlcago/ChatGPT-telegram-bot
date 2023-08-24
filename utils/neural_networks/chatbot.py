import logging

import openai


class ChatBot:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

        # Setup logging
        logging.basicConfig(filename='chatbot.log', level=logging.INFO)

    async def get_response(self, content):
        if not self.model:
            raise ValueError("Model is not specified.")
        try:
            return await self._get_response(content)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            return "Ошибка обработки запроса. Пожалуйста, повторите попытку."

    async def _get_response(self, content):
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
                    "role": "user", "content": content
                }])
        return response.choices[0].message.content.strip()

    async def chat(self, prompt):
        return await self.get_response(prompt)
