from typing import Optional

from pydantic import BaseModel


class ChatMessage(BaseModel):
    role: str
    content: str
    session_id: Optional[str] = None
