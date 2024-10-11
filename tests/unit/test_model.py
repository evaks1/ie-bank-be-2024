from iebank_api.models import Account
import pytest

def test_create_account():
    """
    GIVEN an Account model
    WHEN a new Account is created
    THEN check the name, account_number, balance, currency, country, status, and created_at fields are defined correctly
    """
    # Add the 'country' argument
    account = Account('John Doe', '€', 'US')
    
    assert account.name == 'John Doe'
    assert account.currency == '€'
    assert account.account_number is not None
    assert account.balance == 0.0
    assert account.country == 'US'  # Ensure that 'country' is properly set
    assert account.status == 'Active'
    assert account.created_at is not None