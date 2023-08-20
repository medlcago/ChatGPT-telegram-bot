import logging
import openai


class ImageGenerator:
    def __init__(self, api_key=None, api_base=None, model=None):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model

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
        if not self.api_base:
            raise ValueError("API Base is not specified.")

        openai.api_key = self.api_key
        openai.api_base = self.api_base
        response = openai.Image.create(
            model=self.model,
            prompt=content,
            n=1,
            size="1024x1024"
        )
        return response['data'][0]['url']

    def generate_image(self, prompt):
        return self.get_response(prompt)
