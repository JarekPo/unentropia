from pydantic import BaseModel


class ChatResponse(BaseModel):
    session_id: str
    response: str
