from pydantic import BaseModel


class ChatResponse(BaseModel):
    session_id: str
    response: str
    user_id: int | str | None = None
