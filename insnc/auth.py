import os
import uuid
import requests

def login_and_get_token():
    login = os.getenv("ALFA_LOGIN")
    auth_env = os.getenv("ALFA_AUTH")
    if not login or not auth_env:
        raise EnvironmentError("Set ALFA_LOGIN and ALFA_AUTH env vars.")

    session = requests.Session()
    session_id = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "X-Lang": "ru",
        "X-Client-App": "desktop/Windows--NT 10.0 10/Firefox--137.0",
        "x-session-id": session_id,
        "X-API-Version": "50",
        "X-Dev-ID": "de040169-0d6c-40e3-b621-a783bf350422",
        "Origin": "https://insnc.by",
        "Referer": "https://insnc.by",
        "User-Agent": "Mozilla/5.0"
    }

    # Step 1: Login
    resp = session.post(
        "https://insync3.alfa-bank.by/web/api/authentication/check-client/credentials",
        headers=headers,
        json={"login": login}
    )
    assert resp.ok and resp.json().get("status") == "SUCCESS"
    print(f"[✓] Login '{login}' accepted")

    # Step 2: Password
    headers["Authorization"] = f"Basic {auth_env}"
    resp = session.get(
        "https://insync3.alfa-bank.by/web/api/authentication/login",
        headers=headers
    )
    assert resp.ok and resp.json().get("status") == "SUCCESS"
    print("[✓] Password accepted")

    # Step 3: Token
    resp = session.get(
        "https://insync3.alfa-bank.by/web/api/authentication/session/token",
        headers=headers
    )
    token = resp.headers.get("authorization")
    assert token and token.startswith("Bearer ")

    headers["Authorization"] = token
    print("[✓] Bearer token received")
    
    return token, headers, session
