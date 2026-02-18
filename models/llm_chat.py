from pydantic import BaseModel


class LLMChat(BaseModel):
    session_id: str
    user_id: str
    messages: list[dict[str, str]]
