# insnc/auth.py

import os
import uuid
import json
import requests

CONFIG_FILE = "config.json"

def load_config():
    # Try to load from config file if it exists
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def login_and_get_token():
    # First try environment variables, then config file
    login = os.getenv("ALFA_LOGIN")
    auth_env = os.getenv("ALFA_AUTH")
    x_client_app = os.getenv("X_CLIENT_APP")
    x_dev_id = os.getenv("X_DEV_ID")

    # Fallback to config file if env vars are not set
    if not all([login, auth_env, x_client_app, x_dev_id]):
        config = load_config()
        login = login or config.get("ALFA_LOGIN")
        auth_env = auth_env or config.get("ALFA_AUTH")
        x_client_app = x_client_app or config.get("X-Client-App")
        x_dev_id = x_dev_id or config.get("X-Dev-ID")

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
