# insnc/main.py

import argparse
import insnc.auth
import insnc.extractor
import insnc.exporter


def handle_history(args, session, headers):
    print(f"[→] Fetching {args.items} history items...")
    operations = insnc.extractor.fetch_operations(session, headers, total_items=args.items)

    if args.export:
        export_path = args.export if isinstance(args.export, str) else "operation_history.xlsx"
        insnc.exporter.export_operations_to_excel(operations, filename=export_path)
    else:
        print("\n=== 💳 Operations ===")
        for op in operations:
            date = op.get("date")
            amount = op.get("amount", {}).get("amount")
            postfix = op.get("amount", {}).get("postfix")
            desc = op.get("description", "")
            print(f"{date} | {desc:<30} {amount:>10.2f} {postfix}")


def handle_balance(args, session, headers):
    print("[→] Fetching account balances...")
    balances = insnc.extractor.fetch_balance(session, headers)

    print("\n=== ⚖️ Account Balances ===")
    for acc in balances:
        print(f"{acc['title']:<25} {acc['amount']:>10.2f} {acc['currency']}")


def handle_package(args, session, headers):
    data = insnc.extractor.get_packet_info(session, headers)
    if not data:
        return

    info = data["packageInfo"]
    print("\n=== 💼 Package Info ===")
    print(f"Title     : {info['title']}")
    print(f"Status    : {info['status']['name']}")
    print(f"Payment   : {info['paymentDescription']}")

    print("\n=== 📋 Conditions for free service ===")
    print(data["conditionsTitle"])
    print(data["conditionsDescription"])
    print()

    for cond in data["conditions"]:
        achieved = "✅" if cond["percent"] >= 1.0 else "⚠️"
        current = cond["currentValue"]["amount"]
        target = cond["endValue"]["amount"]
        postfix = cond["currentValue"]["postfix"] or ""
        print(f"{achieved} {cond['text']:<30} {current:.2f}/{target:.2f} {postfix}")


def handle_loyalty(args, session, headers):
    data = insnc.extractor.get_loyalty_status(session, headers)
    if not data:
        return

    bonus = data["bonusAmount"]
    connected = data["isConnected"]

    print("\n=== 🎁 Loyalty Program Status ===")
    print(f"Connected : {'Yes' if connected else 'No'}")
    print(f"Balance   : {bonus['amount']} {bonus['postfix']}")


def main():
    parser = argparse.ArgumentParser(
        description="Interact with Alfa-Bank web API",
        epilog="""
Examples:
  insnc --balance              Show account balances in console
  insnc --history --items 100  Fetch 100 transactions
  insnc -s -e history.xlsx     Export 50 transactions to Excel file
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--history", "-s", action="store_true", help="Fetch operations history")
    parser.add_argument("--items", "-i", type=int, default=50, help="Number of operations to fetch")
    parser.add_argument("--balance", "-b", action="store_true", help="Fetch balance info")
    parser.add_argument("--export", "-e", nargs="?", const=True, help="Export data to Excel (optional: custom path)")
    parser.add_argument("--package", "-p", action="store_true", help="Show package subscription conditions")
    parser.add_argument("--loyalty_status", action="store_true", help="Show loyalty program bonus balance")

    args = parser.parse_args()

    # Check if any "main" flag is set
    command_flags = {
        "history": handle_history,
        "balance": handle_balance,
        "package": handle_package,
        "loyalty_status": handle_loyalty
    }

    # Check if nothing is selected
    if not any(getattr(args, flag) for flag in command_flags):
        parser.print_help()
        return

    # Run only the requested commands
    token, headers, session = insnc.auth.login_and_get_token()

    for flag, handler in command_flags.items():
        if getattr(args, flag):
            handler(args, session, headers)


if __name__ == "__main__":
    main()
