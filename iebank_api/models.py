from iebank_api import db
import random
import string
from datetime import datetime, timezone

class Account(db.Model):
    __tablename__ = 'account'  # Optional: Explicitly define the table name

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), nullable=False)
    account_number = db.Column(db.String(20), nullable=False, unique=True)
    balance = db.Column(db.Float, nullable=False, default=0.0)
    currency = db.Column(db.String(1), nullable=False, default="€")
    status = db.Column(db.String(10), nullable=False, default="Active")
    country = db.Column(db.String(64), nullable=False)  # Ensure this line exists
    created_at = db.Column(db.DateTime(timezone=True), nullable=False, default=lambda: datetime.now(timezone.utc))

    def __repr__(self):
        return f'<Account {self.account_number}>'

    def __init__(self, name, currency, country):
        self.name = name
        self.account_number = ''.join(random.choices(string.digits, k=20))
        self.currency = currency
        self.country = country
        self.balance = 0.0
        self.status = "Active"
        self.created_at = datetime.now(timezone.utc)

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'account_number': self.account_number,
            'balance': self.balance,
            'currency': self.currency,
            'status': self.status,
            'country': self.country,
            'created_at': self.created_at.isoformat()
        }