import uuid
from typing import Any, Dict, List

from fastapi import APIRouter
from llm.services import llm_chat
from models.chat_completion_response import ChatCompletionResponse

router = APIRouter()

user_sessions: Dict[str, List[Dict[str, Any]]] = {}


def get_or_create_session(session_id: str) -> str:
    if session_id is None:
        session_id = str(uuid.uuid4())
    if session_id not in user_sessions:
        user_sessions[session_id] = []
    return session_id


@router.post("/", response_model=ChatCompletionResponse)
async def chat_completion(chat: ChatCompletionResponse) -> ChatCompletionResponse:
    session_id = get_or_create_session(chat.messages[0].session_id if chat.messages else None)
    chat_history = llm_chat()
    return ChatCompletionResponse(messages=chat_history, session_id=session_id)
