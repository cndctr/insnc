def fetch_operations(session, headers, total_items=50):
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
