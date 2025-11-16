import os

from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, HTTPException, Response
from jose import jwt

from app.auth.google_services import exchange_code_for_tokens, google_auth_url, verify_and_extract_idinfo
from app.auth.tokens import create_access_token, create_refresh_token
from app.user_management.user import create_user, get_user_by_google_sub

JWT_ALG = os.getenv("JWT_ALGORITHM")
JWT_SECRET = os.getenv("JWT_SECRET")
load_dotenv()

router = APIRouter()


@router.get("/auth/google/url")
def auth_url():
    return {"url": google_auth_url()}


@router.get("/auth/google/callback")
async def google_callback(code: str, response: Response):
    google_tokens = await exchange_code_for_tokens(code)

    idinfo = verify_and_extract_idinfo(google_tokens["id_token"])

    sub = idinfo["sub"]
    email = idinfo["email"]
    name = idinfo.get("name")
    avatar = idinfo.get("picture")

    user = get_user_by_google_sub(sub)
    user_id = user[0] if user else create_user(sub, email, name, avatar)

    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)

    response.set_cookie("access", access, httponly=True, secure=True, samesite="None")
    response.set_cookie("refresh", refresh, httponly=True, secure=True, samesite="None")

    return {"ok": True}


@router.get("/me")
def me(access: str = Cookie(None)):
    if not access:
        raise HTTPException(401)

    payload = jwt.decode(access, JWT_SECRET, algorithms=[JWT_ALG])
    return {"user_id": payload["sub"]}
