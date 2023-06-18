import openai

from data.config import OpenAI_API_KEY


def image_generator(prompt):
    try:
        openai.api_key = OpenAI_API_KEY
        response = openai.Image.create(
            prompt=prompt,
            n=1,
            size="1024x1024"
        )
        image_url = response['data'][0]['url']
        return image_url
    except Exception as e:
        print(e)
