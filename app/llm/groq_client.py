import os

from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class GroqClient:
    def __init__(self, api_key: str = None, model: str = None, messages: list = None):
        self.api_key = api_key or os.getenv("GROQ_API_KEY")
        self.model = model or os.getenv("MODEL", "qwen/qwen3-32b")
        self.client = Groq(api_key=self.api_key)
        self.messages = messages or []

    def get_response(self, user_message: str):
        self.messages.append(
            {
                "role": "user",
                "content": user_message,
            }
        )
        chat_completion = self.client.chat.completions.create(
            messages=self.messages,
            model=self.model,
            reasoning_effort="none",  # "none" | "low" | "medium" | "high" - temporarly disabled
        )
        response = chat_completion.choices[0].message.content
        self.messages.append(
            {
                "role": "assistant",
                "content": response,
            }
        )
        return response

    def get_messages(self):
        return self.messages
