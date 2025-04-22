# 🏦 insnc — Alfa-Bank Web API CLI

`insnc` is a command-line tool for accessing your Alfa-Bank account data via the web API used by [insnc.by](https://insnc.by).

---

## 🚀 Features

- 🔐 Secure login using environment variables
- 📜 Fetch transaction history
- 📜 Fetch cards balance
- 💼 Get information about your service package
- 📊 Export to Excel with categorized operations:
  - Приход (Income)
  - Расход (Expense)
  - Перевод (Transfer)

---

## 🛠 Setup

### 1. Clone and install

```bash
git clone https://github.com/cndctr/insnc.git
cd insnc
pip install -r requirements.txt
```
You can install it locally using `pip`

```bash
pip install --editable .
```

### 2. Configure 

Edit config.json

```json
{
  "ALFA_LOGIN": "", # Insert your login
  "ALFA_AUTH": "", # Insert your base64 encoded credentials (login:password)
  "X-Client-App": "desktop/Windows--NT 10.0 10/Firefox--137.0", # Change to your browser value
  "X-Dev-ID": "de040169-0d6c-40e3-b621-a783bf350422" # Change to your value
}
```
How to get base64 encoded credentials? 
 - You can use [base64decode.org](https://www.base64decode.org/) to encode your credentials pair - login:password

How to get "X-Client-App" and "X-Dev-ID"?
 - ...

If you don't want to store your credentials in config file then set environment variables:

```cmd
setx ALFA_LOGIN "your_login"
setx ALFA_AUTH "base64encoded_credentials"
```


---

## 🧪 Usage

```bash
# Fetch 50 recent operations and export to Excel
python main.py --history

# Fetch a custom number of items
python main.py --history --items 100

# Get cards' balance
python main.py --balance
```

Or after setup as CLI:

```bash
insnc --history --items 20
insnc -s -i 20
```

---

## 📝 License

MIT — free for personal & educational use.
