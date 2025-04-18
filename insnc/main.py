# insnc/main.py
import argparse
from insnc.auth import login_and_get_token
from insnc.extractor import fetch_operations, fetch_balance
from insnc.exporter import export_operations_to_excel



def main():
    parser = argparse.ArgumentParser(description="Interact with Alfa-Bank web API")
    parser.add_argument("--history", action="store_true", help="Fetch operations history")
    parser.add_argument("--items", type=int, default=50, help="Number of operations to fetch")
    parser.add_argument("--balance", action="store_true", help="Fetch balance info")
    args = parser.parse_args()

    token, headers, session = login_and_get_token()

    if args.history:
        print(f"[→] Fetching {args.items} history items...")
        operations = fetch_operations(session, headers, total_items=args.items)
        export_operations_to_excel(operations)

    elif args.balance:
        print("[→] Fetching account balances...")
        balances = fetch_balance(session, headers)
        print("\n=== Account Balances ===")
        for acc in balances:
            print(f"{acc['title']:<25} {acc['amount']:>10.2f} {acc['currency']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
