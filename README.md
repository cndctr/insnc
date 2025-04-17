# 🏦 insnc — Alfa-Bank Web API CLI

`insnc` is a command-line tool for accessing your Alfa-Bank account data via the web API used by [insnc.by](https://insnc.by). It supports secure login, history retrieval, and export to Excel — all without using a browser.

---

## 🚀 Features

- 🔐 Secure login using environment variables
- 📜 Fetch transaction history
- 📊 Export to Excel with categorized operations:
  - Приход (Income)
  - Расход (Expense)
  - Перевод (Transfer)
- ⚙️ Modular structure (easy to extend: cards, balances, credits)
- 🧩 CLI interface (`--history`, `--items`, `--balance`)

---

## 🛠 Setup

### 1. Clone and install

```bash
git clone https://github.com/cndctr/insnc.git
cd insnc
pip install -r requirements.txt
```

### 2. Set up environment variables

```bash
export ALFA_LOGIN=your_login
export ALFA_AUTH=$(echo -n "your_login:your_password" | base64)
```

Or on Windows CMD:

```cmd
set ALFA_LOGIN=your_login
set ALFA_AUTH=base64encoded_credentials
```

---

## 🧪 Usage

```bash
# Fetch 50 recent operations and export to Excel
python main.py --history

# Fetch a custom number of items
python main.py --history --items 100

# Future feature: get account balance
python main.py --balance
```

Or after setup as CLI:

```bash
insnc --history --items 50
```

---

## 📝 License

MIT — free for personal & educational use.
