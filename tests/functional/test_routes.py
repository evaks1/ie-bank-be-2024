from iebank_api import app
from iebank_api import db
from iebank_api.models import Account
import pytest

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check the response is valid
    """
    response = testing_client.get('/accounts')
    assert response.status_code == 200

def test_get_accounts(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is requested (GET)
    THEN check that a valid response is returned and the data is correct
    """
    # Create some accounts to fetch
    testing_client.post('/accounts', json={'name': 'Alice', 'currency': '€', 'country': 'France'})
    testing_client.post('/accounts', json={'name': 'Bob', 'currency': '$', 'country': 'USA'})
    
    # Retrieve all accounts
    response = testing_client.get('/accounts')
    assert response.status_code == 200
    data = response.get_json()
    
    assert len(data['accounts']) >= 2  # Check if at least 2 accounts exist
    assert data['accounts'][0]['name'] == 'Alice'
    assert data['accounts'][1]['name'] == 'Bob'


def test_create_account(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST)
    THEN check that a new account is created and the response is valid
    """
    response = testing_client.post('/accounts', json={
        'name': 'John Doe',
        'currency': '€',
        'country': 'Germany'
    })
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['name'] == 'John Doe'
    assert data['currency'] == '€'
    assert data['country'] == 'Germany'


def test_create_account_missing_fields(testing_client):
    """
    GIVEN a Flask application
    WHEN the '/accounts' page is posted to (POST) with missing fields
    THEN check that a 400 Bad Request response is returned
    """
    # Missing 'country' field
    response = testing_client.post('/accounts', json={
        'name': 'John Doe',
        'currency': '€'
    })
    assert response.status_code == 400


def test_get_specific_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a GET request is made to '/accounts/<id>'
    THEN check that the correct account is returned
    """
    # Create an account to retrieve
    response = testing_client.post('/accounts', json={
        'name': 'Charlie',
        'currency': '£',
        'country': 'UK'
    })
    account_id = response.get_json()['id']
    
    # Retrieve the specific account
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['name'] == 'Charlie'
    assert data['currency'] == '£'
    assert data['country'] == 'UK'


def test_update_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a PUT request is made to update an account
    THEN check that the account is updated correctly
    """
    # Create an account to update
    response = testing_client.post('/accounts', json={
        'name': 'Dave',
        'currency': '€',
        'country': 'Spain'
    })
    account_id = response.get_json()['id']
    
    # Update the account
    response = testing_client.put(f'/accounts/{account_id}', json={
        'name': 'David Updated',
        'country': 'Canada'
    })
    assert response.status_code == 200
    data = response.get_json()
    
    assert data['name'] == 'David Updated'
    assert data['country'] == 'Canada'


def test_delete_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a DELETE request is made to delete an account
    THEN check that the account is deleted
    """
    # Create an account to delete
    response = testing_client.post('/accounts', json={
        'name': 'Eve',
        'currency': '€',
        'country': 'Italy'
    })
    account_id = response.get_json()['id']
    
    # Delete the account
    response = testing_client.delete(f'/accounts/{account_id}')
    assert response.status_code == 204
    
    # Verify that the account no longer exists
    response = testing_client.get(f'/accounts/{account_id}')
    assert response.status_code == 404


def test_delete_non_existent_account(testing_client):
    """
    GIVEN a Flask application
    WHEN a DELETE request is made to delete a non-existent account
    THEN check that a 404 Not Found response is returned
    """
    response = testing_client.delete('/accounts/99999')  # Non-existent account ID
    assert response.status_code == 404