# insnc/main.py

import argparse
import insnc.auth
import insnc.extractor
import insnc.exporter
from insnc.exporter import format_date


def handle_history(args, session, headers):
    print(f"[→] Fetching {args.items} history items...")
    operations = insnc.extractor.get_history(session, headers, total_items=args.items)

    if args.export:
        export_path = args.export if isinstance(args.export, str) else "operation_history.xlsx"
        insnc.exporter.export_operations_to_excel(operations, filename=export_path)
    else:
        print("\n=== 💳 Operations ===")
        for op in operations:
            date = format_date(op.get("date"))
            amount = op.get("amount", {}).get("amount")
            postfix = op.get("amount", {}).get("postfix")
            desc = op.get("description", "")
            print(f"{date} | {desc:<30} {amount:>10.2f} {postfix}")


def handle_balance(args, session, headers):
    print("[→] Fetching account balances...")
    balances = insnc.extractor.get_balance(session, headers)

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

def handle_loyalty_history(args, session, headers):
    items = insnc.extractor.get_loyalty_history(session, headers)

    if not items:
        return

    print("\n=== 🎁🧾 Loyalty Program History ===")
    for item in items:

        date = format_date(item.get("date"))
        title = item.get("title", "")
        desc = item.get("description", "")
        primary = item.get("primaryAmount", {})
        additional = item.get("additionalAmount", {})
        tag = item.get("additionalInfo", "")

        print(f"{date} | {title:<30} | {desc:<20} | {primary['amount']:>6} {primary['postfix']} | {additional['amount']:>8} {additional['postfix']} {f'({tag})' if tag else ''}")

def handle_credits(args, session, headers):
    data = insnc.extractor.get_credit_details(session, headers, args.credit)
    if not data:
        exit()

    loan = data["loanCommonData"]
    info = data["generalInfo"]["additionalInformation"]
    paid = data["progressBarDetails"]["currentValue"]["amount"]
    total = data["progressBarDetails"]["endValue"]["amount"]
    rate = info["rate"]["amount"]
    start = format_date(info["startCreditDate"])
    end = format_date(info["endCreditContract"])

    print(f"\n=== 💳 Credit Info: {loan['name']} ===")
    print(f"Start date   : {start}")
    print(f"End date     : {end}")
    print(f"Rate         : {rate}%")
    print(f"Total credit : {total:.2f} BYN")
    print(f"Paid so far  : {paid:.2f} BYN")
    print(f"Remaining    : {data['generalInfo']['fullRepaymentSum']['amount']:.2f} BYN")

def handle_credits_list(args, session, headers):
    credits = insnc.extractor.list_available_credits(session, headers)
    if not credits:
        print("No credits found.")
        return

    print("\n=== 🧾 Available Credits ===")
    for c in credits:
        id_ = c["widgetInfo"]["id"]
        title = c["widgetInfo"]["info"]["title"]
        balance = c["widgetInfo"]["info"]["availableAmount"]["amount"]
        print(f"ID: {id_} | {title:<30} | Available: {balance:.2f}") 

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

    parser.add_argument("--history", "-s", action="store_true", help="Fetch operations history. Default - 50 items")
    parser.add_argument("--items", "-i", type=int, default=50, help="Number of operations to fetch")
    parser.add_argument("--balance", "-b", action="store_true", help="Fetch balance info")
    parser.add_argument("--export", "-e", nargs="?", const=True, help="Export data to Excel (optional: custom path)")
    parser.add_argument("--package", "-p", action="store_true", help="Show package subscription conditions")
    parser.add_argument("--loyalty_status", action="store_true", help="Show loyalty program bonus balance")
    parser.add_argument("--loyalty_history", action="store_true", help="Show loyalty bonus transactions")
    parser.add_argument("--credit", "-c", metavar="ID", help="Show credit details by credit ID")
    parser.add_argument("--list_credits", action="store_true", help="List available credit IDs")



    args = parser.parse_args()

    # Check if any "main" flag is set
    command_flags = {
        "history": handle_history,
        "balance": handle_balance,
        "package": handle_package,
        "loyalty_status": handle_loyalty,
        "loyalty_history": handle_loyalty_history,
        "credit": handle_credits,
        "list_credits": handle_credits_list
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
