import uuid

from fastapi import APIRouter
from llm.services import handle_user_message
from models.chat_request import ChatRequest
from models.chat_response import ChatResponse

router = APIRouter()


@router.post("/", response_model=ChatResponse)
async def chat_completion(chat: ChatRequest) -> ChatResponse:
    session_id = chat.session_id or str(uuid.uuid4())
    response = handle_user_message(session_id, chat.message)
    return ChatResponse(session_id=session_id, response=response)
