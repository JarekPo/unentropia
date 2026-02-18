import datetime

from pydantic import BaseModel


class User(BaseModel):
    user_id: str
    google_sub: str
    username: str | None = None
    email: str
    avatar: str | None = None
    created_at: datetime = datetime.datetime.now(datetime.timezone.utc)


class RefreshToken(BaseModel):
    user_id: str
    token_hash: str
    created_at: datetime = datetime.datetime.now(datetime.timezone.utc)
    expires_at: datetime
    revoked: bool = False
