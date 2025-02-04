from flask import Flask, request
import json

app = Flask(__name__)

file_path = "finance_data.json"

def load_data():
    try:
        with open(file_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"accounts": [], "transactions": [], "budgets": []}

def save_data(data):
    with open(file_path, "w") as file:
        json.dump(data, file, indent=4)

@app.route('/')
def home():
    return "Welcome to the Personal Finance Management API."

# Account APIs
@app.route('/accounts/', methods=["POST"])
def create_account():
    data = request.json
    finance_data = load_data()
    new_account = {
        "account_id": len(finance_data["accounts"]) + 1,
        "name": data["name"],
        "type": data["type"],
        "balance": data.get("balance", 0)
    }
    finance_data["accounts"].append(new_account)
    save_data(finance_data)
    return new_account

@app.route('/accounts/', methods=["GET"])
def list_accounts():
    finance_data = load_data()
    return finance_data["accounts"]

@app.route('/accounts/<int:account_id>/', methods=["GET"])
def get_account(account_id):
    finance_data = load_data()
    account = next((acc for acc in finance_data["accounts"] if acc["account_id"] == account_id), None)
    return account if account else {"msg": "Account not found!"}

@app.route('/accounts/<int:account_id>/', methods=["PUT"])
def update_account(account_id):
    data = request.json
    finance_data = load_data()
    for account in finance_data["accounts"]:
        if account["account_id"] == account_id:
            account.update({
                "name": data.get("name", account["name"]),
                "type": data.get("type", account["type"]),
                "balance": data.get("balance", account["balance"])
            })
            save_data(finance_data)
            return account
    return {"msg": "Account not found!"}

@app.route('/accounts/<int:account_id>/', methods=["DELETE"])
def delete_account(account_id):
    finance_data = load_data()
    account = next((acc for acc in finance_data["accounts"] if acc["account_id"] == account_id), None)
    if account:
        finance_data["accounts"].remove(account)
        save_data(finance_data)
        return {"msg": "Account deleted successfully!"}
    return {"msg": "Account not found!"}

# Transaction APIs
@app.route('/transactions/', methods=["POST"])
def create_transaction():
    data = request.json
    finance_data = load_data()
    new_transaction = {
        "transaction_id": len(finance_data["transactions"]) + 1,
        "account_id": data["account_id"],
        "amount": data["amount"],
        "type": data["type"],
        "description": data.get("description", "")
    }
    finance_data["transactions"].append(new_transaction)
    save_data(finance_data)
    return new_transaction

@app.route('/transactions/', methods=["GET"])
def list_transactions():
    finance_data = load_data()
    return finance_data["transactions"]

@app.route('/transactions/<int:transaction_id>/', methods=["GET"])
def get_transaction(transaction_id):
    finance_data = load_data()
    transaction = next((txn for txn in finance_data["transactions"] if txn["transaction_id"] == transaction_id), None)
    return transaction if transaction else {"msg": "Transaction not found!"}

@app.route('/transactions/<int:transaction_id>/', methods=["PUT"])
def update_transaction(transaction_id):
    data = request.json
    finance_data = load_data()
    for transaction in finance_data["transactions"]:
        if transaction["transaction_id"] == transaction_id:
            transaction.update({
                "amount": data.get("amount", transaction["amount"]),
                "type": data.get("type", transaction["type"]),
                "description": data.get("description", transaction["description"])
            })
            save_data(finance_data)
            return transaction
    return {"msg": "Transaction not found!"}

@app.route('/transactions/<int:transaction_id>/', methods=["DELETE"])
def delete_transaction(transaction_id):
    finance_data = load_data()
    transaction = next((txn for txn in finance_data["transactions"] if txn["transaction_id"] == transaction_id), None)
    if transaction:
        finance_data["transactions"].remove(transaction)
        save_data(finance_data)
        return {"msg": "Transaction deleted successfully!"}
    return {"msg": "Transaction not found!"}

# Budget APIs
@app.route('/budget/', methods=["POST"])
def create_budget():
    data = request.json
    finance_data = load_data()
    new_budget = {
        "budget_id": len(finance_data.get("budgets", [])) + 1,
        "category": data["category"],
        "amount": data["amount"]
    }
    finance_data.setdefault("budgets", []).append(new_budget)
    save_data(finance_data)
    return new_budget

@app.route('/budgets/', methods=["GET"])
def list_budgets():
    finance_data = load_data()
    return finance_data.get("budgets", [])

@app.route('/budgets/<int:budget_id>/', methods=["PUT"])
def update_budget(budget_id):
    data = request.json
    finance_data = load_data()
    for budget in finance_data.get("budgets", []):
        if budget["budget_id"] == budget_id:
            budget.update({
                "category": data.get("category", budget["category"]),
                "amount": data.get("amount", budget["amount"])
            })
            save_data(finance_data)
            return budget
    return {"msg": "Budget not found!"}

@app.route('/budgets/<int:budget_id>/', methods=["DELETE"])
def delete_budget(budget_id):
    finance_data = load_data()
    budgets = finance_data.get("budgets", [])
    budget = next((b for b in budgets if b["budget_id"] == budget_id), None)
    if budget:
        budgets.remove(budget)
        save_data(finance_data)
        return {"msg": "Budget deleted successfully!"}
    return {"msg": "Budget not found!"}

# Additional APIs for Reporting and Transfer
@app.route('/report/total_income/', methods=["GET"])
def total_income():
    finance_data = load_data()
    total_income = sum(txn["amount"] for txn in finance_data["transactions"] if txn["type"] == "income")
    return {"total_income": total_income}

@app.route('/report/total_expense/', methods=["GET"])
def total_expense():
    finance_data = load_data()
    total_expense = sum(txn["amount"] for txn in finance_data["transactions"] if txn["type"] == "expense")
    return {"total_expense": total_expense}

@app.route('/account/<int:account_id>/balance/', methods=["GET"])
def account_balance(account_id):
    finance_data = load_data()
    account = next((acc for acc in finance_data["accounts"] if acc["account_id"] == account_id), None)
    if account:
        return {"balance": account["balance"]}
    return {"msg": "Account not found!"}

@app.route('/account/<int:account_id>/transactions/', methods=["GET"])
def account_transactions(account_id):
    finance_data = load_data()
    transactions = [txn for txn in finance_data["transactions"] if txn["account_id"] == account_id]
    return {"transactions": transactions}

@app.route('/report/monthly/', methods=["GET"])
def monthly_report():
    finance_data = load_data()
    # Generate monthly report (sum by month)
    monthly_summary = {}
    for txn in finance_data["transactions"]:
        month = txn["transaction_id"] // 100  # Example of simplifying the month logic
        if month not in monthly_summary:
            monthly_summary[month] = {"income": 0, "expense": 0}
        if txn["type"] == "income":
            monthly_summary[month]["income"] += txn["amount"]
        else:
            monthly_summary[month]["expense"] += txn["amount"]
    return {"monthly_report": monthly_summary}

@app.route('/transfer/', methods=["POST"])
def transfer_amount():
    data = request.json
    finance_data = load_data()
    from_account = next((acc for acc in finance_data["accounts"] if acc["account_id"] == data["from_account"]), None)
    to_account = next((acc for acc in finance_data["accounts"] if acc["account_id"] == data["to_account"]), None)
    if from_account and to_account and from_account["balance"] >= data["amount"]:
        from_account["balance"] -= data["amount"]
        to_account["balance"] += data["amount"]
        new_transaction = {
            "transaction_id": len(finance_data["transactions"]) + 1,
            "account_id": data["from_account"],
            "amount": -data["amount"],
            "type": "transfer",
            "description": f"Transfer to account {data['to_account']}"
        }
        finance_data["transactions"].append(new_transaction)
        new_transaction = {
            "transaction_id": len(finance_data["transactions"]) + 1,
            "account_id": data["to_account"],
            "amount": data["amount"],
            "type": "transfer",
            "description": f"Transfer from account {data['from_account']}"
        }
        finance_data["transactions"].append(new_transaction)
        save_data(finance_data)
        return {"msg": "Transfer successful!"}
    return {"msg": "Transfer failed!"}

# Additional 5 APIs

@app.route('/account/name/<string:name>/balance/', methods=["GET"])
def get_account_balance_by_name(name):
    finance_data = load_data()
    account = next((acc for acc in finance_data["accounts"] if acc["name"].lower() == name.lower()), None)
    if account:
        return {"balance": account["balance"]}
    return {"msg": "Account not found!"}

@app.route('/report/income/category/<string:category>/', methods=["GET"])
def get_income_by_category(category):
    finance_data = load_data()
    total_income = sum(txn["amount"] for txn in finance_data["transactions"] if txn["type"] == "income" and txn["description"].lower() == category.lower())
    return {"total_income": total_income}

@app.route('/report/expense/category/<string:category>/', methods=["GET"])
def get_expense_by_category(category):
    finance_data = load_data()
    total_expense = sum(txn["amount"] for txn in finance_data["transactions"] if txn["type"] == "expense" and txn["description"].lower() == category.lower())
    return {"total_expense": total_expense}

@app.route('/transactions/month/<int:month>/', methods=["GET"])
def get_transactions_by_month(month):
    finance_data = load_data()
    transactions = [txn for txn in finance_data["transactions"] if txn["transaction_id"] // 100 == month]
    return {"transactions": transactions}

@app.route('/transactions/account/<int:account_id>/category/<string:category>/', methods=["GET"])
def get_transactions_by_account_category(account_id, category):
    finance_data = load_data()
    transactions = [txn for txn in finance_data["transactions"] if txn["account_id"] == account_id and txn["description"].lower() == category.lower()]
    return {"transactions": transactions}

if __name__ == "__main__":
    app.run(debug=True)
