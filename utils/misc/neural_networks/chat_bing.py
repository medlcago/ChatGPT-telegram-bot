import re

from EdgeGPT import Chatbot, ConversationStyle

from data.config import COOKIE_PATH

EDGES = {}
my_conversation_style = ConversationStyle.precise


async def bing_chat(message_text, user_id):
    if user_id not in EDGES:
        EDGES[user_id] = Chatbot(cookie_path=COOKIE_PATH)
    response_dict = await EDGES[user_id].ask(prompt=message_text, conversation_style=my_conversation_style)

    if 'text' in response_dict['item']['messages'][1]:
        response = re.sub(r'\[\^\d\^]', '', response_dict['item']['messages'][1]['text'])
    else:
        response = "Что-то пошло не так. Попробуйте еще раз."

    throttling = response_dict['item']['throttling']
    if 'maxNumUserMessagesInConversation' in throttling and 'numUserMessagesInConversation' in throttling:
        max_num_user_messages_in_conversation = throttling['maxNumUserMessagesInConversation']
        num_user_messages_in_conversation = throttling['numUserMessagesInConversation']
        response += "\n———————\n"
        response += f"Контекст: {num_user_messages_in_conversation} / {max_num_user_messages_in_conversation}"

    if num_user_messages_in_conversation >= max_num_user_messages_in_conversation:
        await EDGES[user_id].reset()
        response += "\nКонтекст был автоматически очищен."

    attributions = response_dict['item']['messages'][1]['sourceAttributions']
    if len(attributions) >= 3:
        response += "\n———————\nИсточники:\n"
        for i in range(3):
            provider_display_name = re.sub(
                r'\[\^\d\^]', '', attributions[i]['providerDisplayName'])
            see_more_url = re.sub(
                r'\[\^\d\^]', '', attributions[i]['seeMoreUrl'])
            response += f"{i + 1}.[{provider_display_name}]({see_more_url})\n"

    return response
