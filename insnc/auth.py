# insnc/auth.py

import os
import uuid
import json
import requests

CONFIG_FILE = "config.json"

def load_config():
    try:
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def login_and_get_token():
    # Load config first
    config = load_config()
    
    # Assign variables: try env first, then config, else None
    login = os.getenv("ALFA_LOGIN") or config.get("ALFA_LOGIN")
    auth_env = os.getenv("ALFA_AUTH") or config.get("ALFA_AUTH")
    x_client_app = os.getenv("X_CLIENT_APP") or config.get("X-Client-App")
    x_dev_id = os.getenv("X_DEV_ID") or config.get("X-Dev-ID")

    # Check for missing values and raise errors
    if not login:
        raise ValueError("Missing ALFA_LOGIN (set as environment variable or in config.json)")
    if not auth_env:
        raise ValueError("Missing ALFA_AUTH (set as environment variable or in config.json)")
    if not x_client_app or not x_dev_id:
        raise ValueError("Missing required headers (X-Client-App, X-Dev-ID)")

    session = requests.Session()
    session_id = str(uuid.uuid4())

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json, text/plain, */*",
        "X-Lang": "ru",
        "Origin": "https://insnc.by",
        "Referer": "https://insnc.by",
        "User-Agent": "Mozilla/5.0",
        "x-session-id": session_id,
        "X-API-Version": "52",
        "X-Client-App": x_client_app,
        "X-Dev-ID": x_dev_id
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
