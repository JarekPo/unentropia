import os

from dotenv import load_dotenv
from fastapi import APIRouter, Cookie, Depends, HTTPException, Response
from fastapi.responses import RedirectResponse
from jose import ExpiredSignatureError, JWTError, jwt
from psycopg.rows import dict_row

from auth.google_services import exchange_code_for_tokens, google_auth_url, verify_and_extract_idinfo
from auth.tokens import create_access_token, create_refresh_token, pwd
from database.connection import pool
from user_management.user import create_user, get_user_by_google_sub, get_user_by_id

JWT_ALG = os.getenv("JWT_ALGORITHM")
JWT_SECRET = os.getenv("JWT_SECRET")
FRONTEND_URL = os.getenv("FRONTEND_URL")

load_dotenv()

router = APIRouter()


@router.get("/url")
def auth_url():
    return {"url": google_auth_url()}


@router.get("/callback")
def google_callback(code: str, response: Response):
    google_tokens = exchange_code_for_tokens(code)
    idinfo = verify_and_extract_idinfo(google_tokens["id_token"])

    sub = idinfo["sub"]
    email = idinfo["email"]
    name = idinfo.get("name")
    avatar = idinfo.get("picture")

    user = get_user_by_google_sub(sub)
    if user:
        user_id = user["user_id"]
    else:
        try:
            user_id = create_user(sub, email, name, avatar)
        except Exception as e:
            raise HTTPException(500, f"User creation failed: {str(e)}")

    access = create_access_token(user_id)
    refresh = create_refresh_token(user_id)

    response = RedirectResponse(url=FRONTEND_URL, status_code=303)
    response.set_cookie("access", access, httponly=True, secure=True, samesite="None")
    response.set_cookie("refresh", refresh, httponly=True, secure=True, samesite="None")
    return response


@router.get("/me")
def me(access: str = Cookie(None)):
    if not access:
        raise HTTPException(401)

    try:
        payload = jwt.decode(access, JWT_SECRET, algorithms=[JWT_ALG])
    except ExpiredSignatureError:
        raise HTTPException(401, "Access token expired")
    except JWTError:
        raise HTTPException(401, "Invalid token")

    user_id = payload["sub"]
    user = get_user_by_id(user_id)

    if not user:
        raise HTTPException(404, "User not found")

    return {
        "id": user["user_id"],
        "email": user["email"],
        "name": user["username"],
        "avatar": user.get("avatar"),
    }


@router.post("/refresh")
def refresh(response: Response, refresh: str = Cookie(None)):
    if not refresh:
        raise HTTPException(401)

    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cur:
            cur.execute("""
                SELECT user_id, token_hash
                FROM refresh_tokens
                WHERE expires_at > NOW()
                AND revoked = FALSE
            """)
            rows = cur.fetchall()

    for row in rows:
        if pwd.verify(refresh, row["token_hash"]):
            user_id = row["user_id"]
            break
    else:
        raise HTTPException(401)

    new_access = create_access_token(user_id)

    response.set_cookie(
        "access",
        new_access,
        httponly=True,
        secure=True,
        samesite="None",
    )

    return {"ok": True}


@router.post("/logout")
def logout(user: str = Depends(me)):
    response = Response(content='{"ok": true}', media_type="application/json")
    response.delete_cookie("access")
    response.delete_cookie("refresh")
    with pool.connection() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                UPDATE refresh_tokens
                SET revoked = TRUE
                WHERE user_id = %(user_id)s
            """,
                {"user_id": user["id"]},
            )
            conn.commit()
    return response
