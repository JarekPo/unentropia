from database.connection import pool
from llm.groq_client import GroqClient

user_sessions = {}


def get_or_create_client(session_id: str) -> GroqClient:
    if session_id not in user_sessions:
        user_sessions[session_id] = GroqClient()
    return user_sessions[session_id]


def handle_user_message(session_id: str, user_message: str, user_id: int | str | None = None) -> str:
    client = get_or_create_client(session_id)
    response = client.get_response(user_message)
    store_message(session_id, user_id, user_message, role="user")
    store_message(session_id, user_id, response, role="assistant")
    return response


def store_message(session_id: str, user_id: str, message: str, role: str) -> None:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chat_messages (session_id, user_id, role, content)
                VALUES (%(session_id)s, %(user_id)s, %(role)s, %(content)s)
                RETURNING message_id
                """,
                {
                    "session_id": session_id,
                    "user_id": user_id,
                    "role": role,
                    "content": message,
                },
            )
        conn.commit()
