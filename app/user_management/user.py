from database.connection import db_conn
from psycopg.rows import dict_row


def create_user(google_sub: str, email: str, name: str | None = None, avatar: str | None = None) -> str:
    with db_conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO users (google_sub, email, username, avatar)
            VALUES (%(google_sub)s, %(email)s, %(username)s, %(avatar)s)
            RETURNING user_id
            """,
            {"google_sub": google_sub, "email": email, "username": name, "avatar": avatar},
        )
        user_id = cur.fetchone()[0]
        db_conn.commit()
    return user_id


def get_user_by_google_sub(google_sub: str) -> dict | None:
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT user_id, google_sub, email, username, avatar
            FROM users
            WHERE google_sub = %(google_sub)s
            """,
            {"google_sub": google_sub},
        )
        row = cur.fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "google_sub": row["google_sub"],
                "email": row["email"],
                "username": row["username"],
                "avatar": row["avatar"],
            }
        db_conn.commit()
    return None


def get_user_by_id(user_id: str) -> dict | None:
    with db_conn.cursor(row_factory=dict_row) as cur:
        cur.execute(
            """
            SELECT user_id, google_sub, email, username, avatar
            FROM users
            WHERE user_id = %(user_id)s
            """,
            {"user_id": user_id},
        )
        row = cur.fetchone()
        if row:
            return {
                "user_id": row["user_id"],
                "google_sub": row["google_sub"],
                "email": row["email"],
                "username": row["username"],
                "avatar": row["avatar"],
            }
        db_conn.commit()
    return None
