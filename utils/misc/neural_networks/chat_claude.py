from loader import client_poe


def chat_claude(prompt):
    try:
        for chunk in client_poe.send_message("a2_2", prompt, with_chat_break=True):
            pass
        return chunk["text"]
    except Exception as e:
        print(e)
        return "Ошибка обработки запроса. Пожалуйста, повторите попытку."
