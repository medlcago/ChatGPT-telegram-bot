import logging

import openai
from data.config import OpenAI_API_BASE


class ChatBot:
    def __init__(self, api_key=None, model=None):
        self.api_key = api_key
        self.api_base = OpenAI_API_BASE
        self.model = model

        # Setup logging
        logging.basicConfig(filename='chatbot.log', level=logging.INFO)

    def get_response(self, content):
        if not self.model:
            raise ValueError("Model is not specified.")
        try:
            return self._get_response(content)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            return "Ошибка обработки запроса. Пожалуйста, повторите попытку."

    def _get_response(self, content):
        if not self.api_key:
            raise ValueError("API Key is not specified.")

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {
                    "role": "user", "content": content
                }]
        )
        return response.choices[0].message.content.strip()

    def chat(self, prompt):
        return self.get_response(prompt)
