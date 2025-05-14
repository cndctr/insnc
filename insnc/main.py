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
    from insnc.extractor import get_credits
    from insnc.exporter import format_date  # if format_date is defined there

    credit_id = None if args.credits is True else args.credits
    credits = get_credits(session, headers, credit_id)

    if not credits:
        print("No credit information found.")
        return

    if credit_id:  # Show detailed view
        data = credits[0]
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
    else:  # List view
        print("\n=== 🧾 Available Credits ===")
        for c in credits:
            widget = c["widgetInfo"]
            id_ = widget["id"]
            title = widget["info"]["title"]
            balance = widget["info"]["availableAmount"]["amount"]
            print(f"ID: {id_} | {title:<30} | Available: {balance:.2f}")


def main():
    parser = argparse.ArgumentParser(
        description="Interact with Alfa-Bank web API",
        epilog="""
Examples:
  insnc --balance              Show account balances in console
  insnc --history --items 100  Fetch 100 transactions
  insnc -s -e history.xlsx     Export 50 transactions to Excel file
  insnc -bspc -ls -lh          Show all available information       
""",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    parser.add_argument("--balance", "-b", action="store_true", help="Fetch balance info")
    parser.add_argument("--history", "-s", action="store_true", help="Fetch operations history. Default - 50 items")
    parser.add_argument("--items", "-i", type=int, default=50, help="Number of operations to fetch")
    parser.add_argument("--export", "-e", nargs="?", const=True, help="Export data to Excel (optional: custom path)")
    parser.add_argument("--package", "-p", action="store_true", help="Show package subscription conditions")
    parser.add_argument("--loyalty_status", "-ls", action="store_true", help="Show loyalty program bonus balance")
    parser.add_argument("--loyalty_history", "-lh", action="store_true", help="Show loyalty bonus transactions")
    parser.add_argument("--credits", "-c", nargs="?", const=True, metavar="ID", help="Show credit details. Use without ID to list all.")


    args = parser.parse_args()

    # Check if any "main" flag is set
    command_flags = {
        "balance": handle_balance,
        "history": handle_history,
        "package": handle_package,
        "loyalty_status": handle_loyalty,
        "loyalty_history": handle_loyalty_history,
        "credits": handle_credits

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
