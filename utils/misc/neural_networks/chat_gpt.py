import openai

from data import config
from data.templates import PROMPT_MESSAGE
from loader import client_poe


def get_response(content):
    response = openai.ChatCompletion.create(
        model=config.model,
        messages=[
            {
                "role": "system", "content": PROMPT_MESSAGE
            },
            {
                "role": "user", "content": content
            }]
    )
    return response.choices[0].message.content.strip()


def chat_gpt_3(prompt):
    openai.api_key = config.OpenAI_API_KEY
    try:
        response = get_response(prompt)
        return response
    except openai.error.RateLimitError:
        return "Достигнут лимит запросов в минуту. Пожалуйста, повторите позже."
    except Exception as e:
        print(e)
        return "Ошибка обработки запроса. Пожалуйста, повторите попытку."


def chat_gpt_4(prompt):
    try:
        for chunk in client_poe.send_message("beaver", prompt, with_chat_break=True):
            pass
        return chunk["text"]
    except Exception as e:
        print(e)
        return "Ошибка обработки запроса. Пожалуйста, повторите попытку."
