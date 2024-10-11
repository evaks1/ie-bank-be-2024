# ie-bank-be-2024/routes.py
from flask import Flask, request
from iebank_api import db, app
from iebank_api.models import Account
from flask import jsonify
@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/skull', methods=['GET'])
def skull():
    text = 'Hi! This is the BACKEND SKULL! 💀 '
    
    text = text +'<br/>Database URL:' + db.engine.url.database
    if db.engine.url.host:
        text = text +'<br/>Database host:' + db.engine.url.host
    if db.engine.url.port:
        text = text +'<br/>Database port:' + db.engine.url.port
    if db.engine.url.username:
        text = text +'<br/>Database user:' + db.engine.url.username
    if db.engine.url.password:
        text = text +'<br/>Database password:' + db.engine.url.password
    return text

@app.route('/accounts', methods=['POST'])
def create_account():
    if 'name' not in request.json or 'currency' not in request.json or 'country' not in request.json:
        return {"error": "Missing required fields"}, 400  # Return a 400 error for missing fields
    
    name = request.json['name']
    currency = request.json['currency']
    country = request.json['country']
    
    account = Account(name, currency, country)
    db.session.add(account)
    db.session.commit()
    return format_account(account)


@app.route('/accounts', methods=['GET'])
def get_accounts():
    accounts = Account.query.all()  # Query all accounts from the database
    return jsonify({'accounts': [format_account(account) for account in accounts]})
    
def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'country': account.country,
        'status': account.status,
        'created_at': account.created_at
    }
@app.route('/accounts/<int:id>', methods=['GET'])
def get_account(id):
    account = db.session.get(Account, id)  # Pass the model class and the ID
    if account is None:
        return {"error": "Account not found"}, 404
    
    return format_account(account)

# Route to update an account
@app.route('/accounts/<int:id>', methods=['PUT'])
def update_account(id):
    account = Account.query.get(id)
    account.name = request.json['name']
    account.country = request.json['country']  # Update country as well
    db.session.commit()
    return format_account(account)

# Route to delete an account
@app.route('/accounts/<int:id>', methods=['DELETE'])
def delete_account(id):
    account = Account.query.get(id)
    if account is None:
        return {"error": "Account not found"}, 404
    db.session.delete(account)
    db.session.commit()
    return format_account(account), 204

# Helper function to format account details
def format_account(account):
    return {
        'id': account.id,
        'name': account.name,
        'account_number': account.account_number,
        'balance': account.balance,
        'currency': account.currency,
        'country': account.country,  # Include country in the response
        'status': account.status,
        'created_at': account.created_at
    }