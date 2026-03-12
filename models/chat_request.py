from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str | None = None
    message: str
    user_id: int | str | None = None
