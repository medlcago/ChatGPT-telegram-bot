import logging
import re
from typing import Optional

import openai
from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled

from bot.exceptions import RequestProcessingError


class SummarizeVideo:
    __slots__ = ("api_key", "api_base", "model", "languages")

    def __init__(self, api_key: str, api_base: str, model: str, languages=("ru", "en", "de", "es")):
        self.api_key = api_key
        self.api_base = api_base
        self.model = model
        self.languages = languages

    def get_response(self, text: str, language: str) -> str:
        if not self.model:
            raise ValueError("Model is not specified.")
        try:
            return self._get_response(text=text, language=language)
        except Exception as e:
            logging.error(f'Error processing request: {e}')
            raise RequestProcessingError("Error processing request. Please, try again.")

    def _get_response(self, text: str, language: str) -> str:
        if not self.api_key:
            raise ValueError("API Key is not specified.")
        if not self.api_base:
            raise ValueError("API Base is not specified.")

        openai.api_key = self.api_key
        openai.api_base = self.api_base

        instructions_map = {
            "ru": "Пожалуйста, резюмируйте предоставленный текст на русском языке",
            "en": "Please, summarize the provided text in English"
        }

        prompt = instructions_map.get(language, instructions_map["en"])

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=[
                {"role": "system", "content": prompt},
                {"role": "user", "content": text}
            ],
            temperature=0.2,
            n=1,
            max_tokens=4096,
            presence_penalty=0,
            frequency_penalty=0.1,
        )
        return response.choices[0].message.content.strip()

    @staticmethod
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

    def get_video_transcript(self, video_id: str) -> Optional[str]:
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id=video_id, languages=self.languages)
        except TranscriptsDisabled:
            return

        text = " ".join([line["text"] for line in transcript])
        return text

    def generate_summary(self, text: str, language: str) -> str:
        return self.get_response(text=text, language=language)

    def summarize_youtube_video(self, video_url: str, language: str = "ru") -> str:
        video_id = self.extract_youtube_video_id(url=video_url)

        if video_id is None:
            return "Ссылка не является ссылкой на видео с YouTube"

        transcript = self.get_video_transcript(video_id=video_id)

        if transcript is None:
            return f"Для данного видео нет транскрипта на английском или русском языке: {video_url}"

        summary = self.generate_summary(text=transcript, language=language)

        return summary
