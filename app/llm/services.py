from llm.groq_client import GroqClient

user_sessions = {}


def get_or_create_client(session_id: str) -> GroqClient:
    if session_id not in user_sessions:
        user_sessions[session_id] = GroqClient()
    return user_sessions[session_id]


def handle_user_message(session_id: str, user_message: str) -> str:
    client = get_or_create_client(session_id)
    response = client.get_response(user_message)
    return response
