import logging

import openai
import poe

from data import config
from data.templates import PROMPT_MESSAGE


class ChatBot:
    def __init__(self, api_key=None, poe_token=None, model=None):
        self.api_key = api_key
        self.poe_token = poe_token
        self.model = model

        # Setup logging
        logging.basicConfig(filename='chatbot.log', level=logging.INFO)

    def get_response(self, content):
        if not self.model:
            raise ValueError("Model is not specified.")

        try:
            if self.model == "gpt-3.5-turbo":
                return self.get_response_gpt3(content)
            elif self.model == "gpt-4" or self.model == "claude":
                return self.get_response_poe(content)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            return "Ошибка обработки запроса. Пожалуйста, повторите попытку."

    def get_response_gpt3(self, content):
        if not self.api_key:
            raise ValueError("API Key is not specified.")
        openai.api_key = self.api_key
        response = openai.ChatCompletion.create(
            model=config.models[self.model],
            messages=[
                {
                    "role": "system", "content": PROMPT_MESSAGE
                },
                {
                    "role": "user", "content": content
                }]
        )
        return response.choices[0].message.content.strip()

    def get_response_poe(self, content):
        if not self.poe_token:
            raise ValueError("POE Token is not specified.")
        client_poe = poe.Client(token=self.poe_token)
        client_poe.formkey_salt = "f09"
        for response in client_poe.send_message(config.models[self.model], content, with_chat_break=True):
            pass
        client_poe.disconnect_ws()
        return response["text"]

    def chat(self, prompt):
        return self.get_response(prompt)
