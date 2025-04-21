# insnc/auth.py

import os
import uuid
import json
import requests

CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"{CONFIG_FILE} not found. Please create it and add your credentials and headers.")
    
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def login_and_get_token():
    config = load_config()

    # Fallback: if values are empty in config.json, try env vars
    login = config.get("ALFA_LOGIN") or os.getenv("ALFA_LOGIN")
    auth_env = config.get("ALFA_AUTH") or os.getenv("ALFA_AUTH")
    x_client_app = config.get("X-Client-App")
    x_dev_id = config.get("X-Dev-ID")

    if not login:
        raise ValueError("Missing ALFA_LOGIN (in config.json or env)")
    if not auth_env:
        raise ValueError("Missing ALFA_AUTH (in config.json or env)")
    if not x_client_app or not x_dev_id:
        raise ValueError("Missing required headers (X-Client-App, X-Dev-ID) in config.json")

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
        "X-API-Version": "50",
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
