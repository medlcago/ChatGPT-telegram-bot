import poe

from data import config


def get_response(content, model):
    try:
        client_poe = poe.Client(token=config.POE_TOKEN)
        for response in client_poe.send_message(config.models[model], content, with_chat_break=True):
            pass
        client_poe.disconnect_ws()
        return response["text"]
    except Exception as e:
        print(e)
        return "Ошибка обработки запроса. Пожалуйста, повторите попытку."


def chat_claude(prompt):
    response = get_response(prompt, model="claude")
    return response
