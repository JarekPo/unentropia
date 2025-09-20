import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


class GroqClient:
    def __init__(self, api_key: str = None, model: str = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv("MODEL", "qwen/qwen3-32b")
        self.client = Groq(api_key=self.api_key)

    def get_response(self, user_message: str):
        chat_completion = self.client.chat.completions.create(
            messages=[{"role": "user", "content": user_message}], model=self.model
        )
        return chat_completion.choices[0].message.content
