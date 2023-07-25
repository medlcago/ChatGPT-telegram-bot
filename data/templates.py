DEBUG_MESSAGE = "Technical work is underway. The bot is temporarily unavailable."

START_MESSAGE = {
    "ru": """Привет, {username}!

Этот бот открывает вам доступ к ChatGPT и Dall-E для создания текста и изображений.

Бот использует модели gpt-3.5-turbo/gpt-4

Чатбот умеет:
1. Создавать изображения
2. Писать и редактировать тексты
3. Переводить с любого языка на любой
4. Писать и редактировать код
5. Отвечать на вопросы
6. Делать саммари из YouTube-видео

Вы можете общаться с ботом, как с живым собеседником, задавая вопросы на любом языке. Обратите внимание, что иногда бот придумывает факты, а также обладает ограниченными знаниями о событиях после 2021 года.

✉️ Чтобы получить текстовый ответ, просто напишите в чат ваш вопрос.

🌅 Чтобы создать изображение, начните запрос с команды /image, а затем добавьте описание.

🎬 Чтобы сделать саммари из YouTube-видео, используйте команду /summary, а затем через пробел ссылку на видео.""",
    "en": """Hello, {username}!

This bot gives you access to ChatGPT and Dall-E to create text and images.

Bot uses gpt-3.5-turbo/gpt-4 models

Chatbot can:
1. Create images
2. Write and edit texts
3. Translate from any language to any
4. Write and edit code
5. Answer questions
6. Make summaries from YouTube videos

You can communicate with the bot, as with a live interlocutor, asking questions in any language. Please note that sometimes the bot makes up facts and also has limited knowledge of events after 2021.

✉️ To get a text answer, just write your question in the chat.

🌅 To create an image, start a request with the /image command and then add a description.

🎬 To make a summary of a YouTube video, use the /summary command, followed by a link to the video separated by a space."""
}

PROMPT_MESSAGE = """Ты полезный ассистент с ИИ, который готов помочь своему пользователю.
Ты даешь короткие содержательные ответы, обычно не более 100 символов.
Если я попрошу тебя написать код, пиши его на python, код присылай без объяснений.
Если программа должна возвращать какой-то результат, то выводи его с помощью print.
Не используй в коде ключи для доступа и токены.
Если присылаешь код, то пожалуйста, форматируй его markdown
Используй библиотеку yfinance для доступа к ценам акций
Для работы с вопросами о погоде используй python_weather"""

MODELS = f"""Доступные модели:
gpt-4
gpt-3.5-turbo
claude
bing
"""
