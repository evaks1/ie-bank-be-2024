from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from dotenv import load_dotenv
import os

# Initialize the Flask application
app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Select configuration based on the ENV environment variable
env = os.getenv('ENV', 'production')  # Default to 'production' if ENV not set
if env == 'local':
    print("Running in local mode")
    app.config.from_object('config.LocalConfig')
elif env == 'dev':
    print("Running in development mode")
    app.config.from_object('config.DevelopmentConfig')
elif env == 'ghci':
    print("Running in GitHub CI mode")
    app.config.from_object('config.GithubCIConfig')
else:
    print("Running in production mode")
    app.config.from_object('config.ProductionConfig')

# Initialize SQLAlchemy without binding it to the app yet
db = SQLAlchemy()

# Initialize CORS
CORS(app)

# Import models here to ensure they are registered with SQLAlchemy before creating tables
from iebank_api.models import Account

# Import routes after models to avoid circular imports
from iebank_api import routes

# Bind SQLAlchemy to the app
db.init_app(app)

# Create database tables within the app context
with app.app_context():
    db.create_all()

    # Debugging: List tables and columns to verify
    from sqlalchemy import inspect

    inspector = inspect(db.engine)
    tables = inspector.get_table_names()
    print("Tables:", tables)

    if 'account' in tables:
        columns = [column['name'] for column in inspector.get_columns('account')]
        print("Columns in 'account':", columns)
    else:
        print("'account' table does not exist")