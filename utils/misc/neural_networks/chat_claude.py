from data import config
from loader import client_poe


def get_response(content, model):
    try:
        for response in client_poe.send_message(config.models[model], content, with_chat_break=True):
            pass
        return response["text"]
    except Exception as e:
        print(e)
        return "Ошибка обработки запроса. Пожалуйста, повторите попытку."


def chat_claude(prompt):
    response = get_response(prompt, model="claude")
    return response
