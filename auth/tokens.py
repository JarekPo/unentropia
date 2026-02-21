import datetime
import os
import secrets

from jose import jwt
from passlib.context import CryptContext

from database.connection import pool

JWT_ALG = os.getenv("JWT_ALGORITHM")
JWT_EXPIRE_MIN = int(os.getenv("ACCESS_TOKEN_EXPIRES_MIN", 15))
JWT_SECRET = os.getenv("JWT_SECRET")
REFRESH_TOKEN_EXPIRES_DAYS = int(os.getenv("REFRESH_TOKEN_EXPIRES_DAYS", 30))


pwd = CryptContext(schemes=["sha256_crypt"], deprecated="auto")


def create_access_token(user_id: int):
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=JWT_EXPIRE_MIN)
    return jwt.encode({"sub": str(user_id), "exp": expire}, JWT_SECRET, algorithm=JWT_ALG)


def create_refresh_token(user_id: int):
    raw = secrets.token_urlsafe(64)
    hashed = pwd.hash(raw)
    token_exp = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(days=REFRESH_TOKEN_EXPIRES_DAYS)

    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO refresh_tokens (user_id, token_hash, expires_at) VALUES (%(user_id)s, %(token_hash)s, %(expires_at)s)",
                {"user_id": user_id, "token_hash": hashed, "expires_at": token_exp},
            )
        conn.commit()

    return raw
