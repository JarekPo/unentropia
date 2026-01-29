import os

import requests
from dotenv import load_dotenv
from fastapi import HTTPException
from google.auth.transport import requests as google_requests
from google.oauth2 import id_token

load_dotenv()

GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")
GOOGLE_REDIRECT_URI = os.getenv("GOOGLE_REDIRECT_URI")


def google_auth_url():
    base = "https://accounts.google.com/o/oauth2/v2/auth"
    params = (
        f"client_id={GOOGLE_CLIENT_ID}"
        f"&redirect_uri={GOOGLE_REDIRECT_URI}"
        "&response_type=code"
        "&scope=openid%20email%20profile"
        "&prompt=consent"
        "&access_type=offline"
    )
    return f"{base}?{params}"


def exchange_code_for_tokens(code: str):
    token_url = "https://oauth2.googleapis.com/token"

    resp = requests.post(
        token_url,
        data={
            "code": code,
            "client_id": GOOGLE_CLIENT_ID,
            "client_secret": GOOGLE_CLIENT_SECRET,
            "redirect_uri": GOOGLE_REDIRECT_URI,
            "grant_type": "authorization_code",
        },
        timeout=10,
    )

    data = resp.json()

    if "id_token" not in data:
        raise HTTPException(401, "Google rejected code")

    return data


def verify_and_extract_idinfo(raw_id_token: str):
    try:
        return id_token.verify_oauth2_token(
            raw_id_token,
            google_requests.Request(),
            GOOGLE_CLIENT_ID,
        )
    except Exception:
        raise HTTPException(401, "Invalid Google id_token")
