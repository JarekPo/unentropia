import datetime
import os
import secrets

import psycopg
from jose import jwt
from passlib.context import CryptContext

JWT_ALG = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", 15))
JWT_SECRET = os.getenv("JWT_SECRET")
DATABASE_URL = os.getenv("DATABASE_URL")

db_conn = psycopg.connect(DATABASE_URL)

pwd = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(user_id: int):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=JWT_EXPIRE_MIN)
    return jwt.encode({"sub": str(user_id), "exp": expire}, JWT_SECRET, algorithm=JWT_ALG)


def create_refresh_token(user_id: int):
    raw = secrets.token_urlsafe(64)
    hashed = pwd.hash(raw)

    cur = db_conn.cursor()
    cur.execute(
        "INSERT INTO refresh_tokens (user_id, token_hash) VALUES (%(user_id)s, %(token_hash)s)",
        {"user_id": user_id, "token_hash": hashed},
    )
    db_conn.commit()

    return raw


def verify_refresh(user_id: int, raw_refresh: str):
    cur = db_conn.cursor()
    cur.execute(
        "SELECT token_hash FROM refresh_tokens WHERE user_id=%(user_id)s ORDER BY id DESC LIMIT 1", {"user_id": user_id}
    )
    row = cur.fetchone()
    if not row:
        return False

    stored_hash = row["token_hash"]
    return pwd.verify(raw_refresh, stored_hash)
