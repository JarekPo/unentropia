from database.connection import pool
from psycopg.rows import dict_row


def create_user(google_sub: str, email: str, name: str | None = None, avatar: str | None = None) -> str:
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO users (google_sub, email, username, avatar)
                VALUES (%(google_sub)s, %(email)s, %(username)s, %(avatar)s)
                RETURNING user_id
                """,
                {
                    "google_sub": google_sub,
                    "email": email,
                    "username": name,
                    "avatar": avatar,
                },
            )
            user_id = cur.fetchone()[0]
        conn.commit()

    return user_id


def get_user_by_google_sub(google_sub: str) -> dict | None:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT user_id, google_sub, email, username, avatar
                FROM users
                WHERE google_sub = %(google_sub)s
                """,
                {"google_sub": google_sub},
            )
            return cur.fetchone()


def get_user_by_id(user_id: str) -> dict | None:
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute(
                """
                SELECT user_id, google_sub, email, username, avatar
                FROM users
                WHERE user_id = %(user_id)s
                """,
                {"user_id": user_id},
            )
            return cur.fetchone()
