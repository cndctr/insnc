# insnc/main.py
import argparse
from insnc.auth import login_and_get_token
from insnc.extractor import fetch_operations, fetch_balance
from insnc.exporter import export_operations_to_excel



def main():
    parser = argparse.ArgumentParser(
        description="Interact with Alfa-Bank web API",
        epilog="""
Examples:
  insnc --history              Fetch recent 50 transactions
  insnc --history --items 100  Fetch 100 transactions
  insnc --balance              Show account balances in console
  insnc --history -e           Export recent 50 transactions to Excel
  insnc --history -e custom.xlsx  Export to custom path
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument("--history", action="store_true", help="Fetch operations history")
    parser.add_argument("--items", type=int, default=50, help="Number of operations to fetch")
    parser.add_argument("--balance", action="store_true", help="Fetch balance info")
    parser.add_argument("--export", "-e", nargs="?", const=True, help="Export data to Excel (optional: custom path)")
    args = parser.parse_args()

    if not args.history and not args.balance:
        parser.print_help()
        return

    token, headers, session = login_and_get_token()

    if args.history:
        print(f"[→] Fetching {args.items} history items...")
        operations = fetch_operations(session, headers, total_items=args.items)

        if args.export:
            export_path = args.export if isinstance(args.export, str) else "operation_history.xlsx"
            export_operations_to_excel(operations, filename=export_path)
        else:
            print("\n=== Operations ===")
            for op in operations:
                date = op.get("date")
                amount = op.get("amount", {}).get("amount")
                postfix = op.get("amount", {}).get("postfix")
                desc = op.get("description", "")
                print(f"{date} | {desc:<30} {amount:>10.2f} {postfix}")

    elif args.balance:
        print("[→] Fetching account balances...")
        balances = fetch_balance(session, headers)

        print("\n=== Account Balances ===")
        for acc in balances:
            print(f"{acc['title']:<25} {acc['amount']:>10.2f} {acc['currency']}")


if __name__ == "__main__":
    main()