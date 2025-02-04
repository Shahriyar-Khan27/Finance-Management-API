# Personal Finance Management API

A Flask-based REST API for managing personal finances, including accounts, transactions, and budgets.

## Setup and Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd personal-finance-api
```

2. Install required dependencies:
```bash
pip install flask
```

3. Run the application:
```bash
python app.py
```

The server will start running on `http://localhost:5000`

## API Endpoints

### Home
- `GET /` - Welcome message

### Account Management
- `GET /accounts/` - List all accounts
- `POST /accounts/` - Create new account
- `GET /accounts/<account_id>/` - Get specific account details
- `PUT /accounts/<account_id>/` - Update account details
- `DELETE /accounts/<account_id>/` - Delete an account
- `GET /account/<account_id>/balance/` - Get account balance
- `GET /account/name/<name>/balance/` - Get account balance by name

### Transaction Management
- `GET /transactions/` - List all transactions
- `POST /transactions/` - Create new transaction
- `GET /transactions/<transaction_id>/` - Get specific transaction
- `PUT /transactions/<transaction_id>/` - Update transaction
- `DELETE /transactions/<transaction_id>/` - Delete transaction
- `GET /account/<account_id>/transactions/` - Get account transactions
- `GET /transactions/month/<month>/` - Get transactions by month
- `GET /transactions/account/<account_id>/category/<category>/` - Get transactions by account and category

### Budget Management
- `GET /budgets/` - List all budgets
- `POST /budget/` - Create new budget
- `PUT /budgets/<budget_id>/` - Update budget
- `DELETE /budgets/<budget_id>/` - Delete budget

### Reports
- `GET /report/total_income/` - Get total income
- `GET /report/total_expense/` - Get total expense
- `GET /report/monthly/` - Get monthly report
- `GET /report/income/category/<category>/` - Get income by category
- `GET /report/expense/category/<category>/` - Get expense by category

### Transfer
- `POST /transfer/` - Transfer amount between accounts

## API Usage Examples

### Create Account
```bash
POST /accounts/
Content-Type: application/json

{
    "name": "Savings Account",
    "type": "savings",
    "balance": 5000
}
```

### Create Transaction
```bash
POST /transactions/
Content-Type: application/json

{
    "account_id": 1,
    "amount": 1000,
    "type": "income",
    "description": "Salary"
}
```

### Create Budget
```bash
POST /budget/
Content-Type: application/json

{
    "category": "Groceries",
    "amount": 300
}
```

### Transfer Money
```bash
POST /transfer/
Content-Type: application/json

{
    "from_account": 1,
    "to_account": 2,
    "amount": 500
}
```

## Data Structure

### Account Object
```json
{
    "account_id": 1,
    "name": "Savings Account",
    "type": "savings",
    "balance": 5000
}
```

### Transaction Object
```json
{
    "transaction_id": 1,
    "account_id": 1,
    "amount": 1000,
    "type": "income",
    "description": "Salary"
}
```

### Budget Object
```json
{
    "budget_id": 1,
    "category": "Groceries",
    "amount": 300
}
```

## Error Handling

The API returns appropriate HTTP status codes:
- 200: Success
- 404: Resource not found
- 400: Bad request

Error responses include a message explaining the error.

## File Structure
```
personal-finance-api/
├── app.py
├── finance_data.json
└── README.md
```
