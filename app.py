# app.py

from iebank_api import app

if __name__ == '__main__':
    app.run(debug=True, port=8080)  # Specify port if needed