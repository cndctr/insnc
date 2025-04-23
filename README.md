# 🏦 insnc — Alfa-Bank Web API CLI

`insnc` is a command-line tool for accessing your Alfa-Bank account data via the web API used by [insnc.by](https://insnc.by).

---

## 🚀 Features

- 🔐 Secure login using environment variables
- 📜 Fetch transaction history
- 📜 Fetch cards balance
- 💼 Get information about your service package
- 🎁 Get information about youy loyalty program (status and history)
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
1. When you log in to [insnc.by](https://insnc.by) in your browser for the first time, the bank will prompt you with the second step of 2FA and display a QR code on the screen.  
   You must scan this code using the **Insync mobile app** — this authorizes the new device and browser. After successful login, you can capture the required parameters as follows:
2. Open [insnc.by](https://insnc.by) in your browser and open **Developer Tools** (`Ctrl+Shift+I`). Switch to the **Network** tab.
3. Enter your login and click **"Продолжить"**. You should see some network activity.
4. Look for the `POST` request related to login credentials — select it.
5. In the **Request Headers**, find `X-Client-App` and `X-Dev-ID`. Copy these values and paste them into your `config.json` file.
Example:


![image](https://github.com/user-attachments/assets/1a24854b-85b0-44e7-9d32-767a9b392550)


What if you don't want to store your credentials in config.json?
 -  Then set environment variables:

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

# Fetch loyalty program status and history
python main.py --loyalty_status --loyalty_history
```

Or after setup using pip locally:

```bash
insnc --history --items 20
insnc -s -i 20
```

---

## 📝 License

MIT — free for personal & educational use.
