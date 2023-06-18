import openai
import re
from openai import InvalidRequestError
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from data import config


def extract_youtube_video_id(url: str) -> str | None:
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


def get_video_transcript(video_id: str) -> str | None:
    """
    Fetch the transcript of the provided YouTube video
    """
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=["ru", "en", "de", "es"])
    except TranscriptsDisabled:
        # The video doesn't have a transcript
        return None

    text = " ".join([line["text"] for line in transcript])
    return text


def generate_summary(text: str, language="ru") -> str:
    """
    Generate a summary of the provided text using OpenAI API
    """
    openai.api_key = config.OpenAI_API_KEY

    # Use GPT to generate a summary
    instructions = "Пожалуйста, резюмируйте предоставленный текст на русском языке" if language == "ru" else "Please, summarize the provided text in English"
    try:
        response = openai.ChatCompletion.create(
            model=config.model,
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

        # Return the generated summary
        return response.choices[0].message.content.strip()
    except InvalidRequestError as error:
        print(error)
        return "К сожалению, превышена максимальная длина сообщения :(" if language == "ru" else "Unfortunately, the maximum message length has been exceeded :("


def summarize_youtube_video(video_url: str, language="ru") -> str:
    """
    Summarize the provided YouTube video
    """
    # Extract the video ID from the URL
    video_id = extract_youtube_video_id(video_url)

    # Fetch the video transcript
    if not video_id:
        return "The link is not a link to a youtube video"
    transcript = get_video_transcript(video_id)

    # If no transcript is found, return an error message
    if not transcript:
        return f"No transcript found for this video in English or Russian: {video_url}"

    summary = generate_summary(transcript, language=language)

    return summary
