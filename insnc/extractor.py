def get_history(session, headers, total_items=50):
    page_size = total_items
    pages = 1

    all_items = []

    for page in range(pages):
        offset = page * page_size
        payload = {
            "pageSize": page_size,
            "offset": offset
        }

        response = session.post(
            "https://insync3.alfa-bank.by/web/api/history/items",
            headers=headers,
            json=payload
        )

        if not response.ok:
            print(f"[✗] Failed to fetch page {page + 1}")
            continue

        items = response.json().get("items", [])
        if not items:
            break

        all_items.extend(items)

    return all_items

def get_balance(session, headers):
    response = session.get(
        "https://insync3.alfa-bank.by/web/api/account/list",
        headers=headers
    )

    if not response.ok:
        print(f"[✗] Failed to fetch balance: {response.status_code}")
        return []

    accounts = response.json().get("accounts", [])
    balances = []

    for acc in accounts:
        try:
            info = acc["widgetInfo"]["info"]
            balances.append({
                "title": info.get("title", ""),
                "amount": info["amount"]["amount"],
                "currency": info["amount"]["postfix"]
            })
        except (KeyError, TypeError):
            continue

    return balances

def get_packet_info(session, headers):
    response = session.get(
        "https://insync3.alfa-bank.by/web/api/package-solution/info",
        headers=headers
    )

    if not response.ok:
        print("[✗] Failed to retrieve package info.")
        return None

    return response.json()

def get_loyalty_status(session, headers):
    response = session.get(
        "https://insync3.alfa-bank.by/web/api/loyalty-program/status",
        headers=headers
    )

    if not response.ok:
        print("[✗] Failed to retrieve loyalty program status.")
        return None

    return response.json()

def get_loyalty_history(session, headers, page_size=20, offset=0):
    payload = {
        "pageSize": page_size,
        "offset": offset,
        "filter": {}
    }

    response = session.post(
        "https://insync3.alfa-bank.by/web/api/loyalty-program/history",
        headers=headers,
        json=payload
    )

    if not response.ok:
        print("[✗] Failed to retrieve loyalty history")
        return []

    return response.json().get("items", [])


def get_credits(session, headers, credit_id=None):
    list_response = session.get(
        "https://insync3.alfa-bank.by/web/api/credit-details/list",
        headers=headers
    )

    if not list_response.ok:
        print(f"[✗] Failed to fetch credit list: {list_response.status_code}")
        return []

    credits = list_response.json().get("credits", [])

    # If a specific ID is requested, filter to that one
    if credit_id:
        credits = [c for c in credits if c.get("widgetInfo", {}).get("id") == credit_id]

    result = []
    for credit in credits:
        cid = credit.get("widgetInfo", {}).get("id")
        detail_response = session.get(
            f"https://insync3.alfa-bank.by/web/api/credit-details/info?id={cid}",
            headers=headers
        )
        if detail_response.ok:
            data = detail_response.json()
            data["widgetInfo"] = credit.get("widgetInfo", {})
            result.append(data)
        else:
            print(f"[!] Failed to fetch credit details for ID {cid}")

    return result

