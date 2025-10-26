from typing import List, Optional

from pydantic import BaseModel

from .chat_message import ChatMessage


class ChatCompletionResponse(BaseModel):
    messages: List[ChatMessage]
    session_id: Optional[str] = None
