import pytest
from iebank_api import db, app


@pytest.fixture(scope='function')
def testing_client():
    # Configure the app for testing
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Use in-memory DB for tests
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()  # Create tables based on models

        # Debugging: List tables and columns to verify
        from sqlalchemy import inspect

        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        print("Test DB Tables:", tables)

        if 'account' in tables:
            columns = [column['name'] for column in inspector.get_columns('account')]
            print("Test DB Columns in 'account':", columns)
        else:
            print("'account' table does not exist in test DB")

        yield app.test_client()  # Provide the test client to the test

        db.session.remove()
        db.drop_all()  # Clean up after the test