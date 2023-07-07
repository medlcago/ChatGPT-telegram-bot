import openai
import re
from openai import InvalidRequestError
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled
from typing import Optional
from data import config


def extract_youtube_video_id(url: str) -> Optional[str]:
    """
    Links example:
    1. 'https://www.youtube.com/watch?v=video_id',
    2. 'https://m.youtube.com/watch?v=video_id',
    3. 'https://youtu.be/video_id',
    4. 'https://www.youtube.com/embed/video_id',
    """
    match = re.search(r'(?:youtube\.com/(?:watch\?v=|embed/)|youtu\.be/)([a-zA-Z0-9_-]+)', url)
    if match:
        video_id = match.group(1)
        return video_id


def get_video_transcript(video_id: str) -> Optional[str]:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=["ru", "en", "de", "es"])
    except TranscriptsDisabled:
        return None

    text = " ".join([line["text"] for line in transcript])
    return text


def configure_openai_api():
    openai.api_key = config.OpenAI_API_KEY


def generate_summary(text: str, language: str = "ru") -> str:
    configure_openai_api()

    instructions_map = {
        "ru": "Пожалуйста, резюмируйте предоставленный текст на русском языке",
        "en": "Please, summarize the provided text in English"
    }

    instructions = instructions_map.get(language, instructions_map["en"])

    try:
        response = openai.ChatCompletion.create(
            model=config.models["gpt-3"],
            messages=[
                {"role": "system", "content": instructions},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            n=1,
            max_tokens=200,
            presence_penalty=0,
            frequency_penalty=0.1,
        )

        return response.choices[0].message.content.strip()
    except InvalidRequestError as error:
        print(error)
        return "К сожалению, превышена максимальная длина сообщения :(" if language == "ru" else "Unfortunately, the maximum message length has been exceeded :("


def summarize_youtube_video(video_url: str, language: str = "ru") -> str:
    video_id = extract_youtube_video_id(video_url)

    if not video_id:
        return "Ссылка не является ссылкой на видео с YouTube"

    transcript = get_video_transcript(video_id)

    if not transcript:
        return f"Для данного видео нет транскрипта на английском или русском языке: {video_url}"

    summary = generate_summary(transcript, language=language)

    return summary