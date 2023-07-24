import openai
import poe

from data import config
from data.templates import PROMPT_MESSAGE


def get_response(content, model):
    try:
        if model == "gpt-3":
            response = openai.ChatCompletion.create(
                model=config.models[model],
                messages=[
                    {
                        "role": "system", "content": PROMPT_MESSAGE
                    },
                    {
                        "role": "user", "content": content
                    }]
            )
            return response.choices[0].message.content.strip()
        elif model == "gpt-4":
            client_poe = poe.Client(token=config.POE_TOKEN)
            client_poe.formkey_salt = "f09"
            for response in client_poe.send_message(config.models[model], content, with_chat_break=True):
                pass
            client_poe.disconnect_ws()
            return response["text"]
    except Exception as e:
        print(e)
        return "Ошибка обработки запроса. Пожалуйста, повторите попытку."


def chat_gpt_3(prompt):
    openai.api_key = config.OpenAI_API_KEY
    response = get_response(prompt, model="gpt-3")
    return response


def chat_gpt_4(prompt):
    response = get_response(prompt, model="gpt-4")
    return response
