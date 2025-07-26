
import os

def load_config():
    os.environ['OANDA_API_KEY'] = os.getenv('OANDA_API_KEY', 'your-api-key')
    os.environ['OANDA_ACCOUNT_ID'] = os.getenv('OANDA_ACCOUNT_ID', 'your-account-id')
    os.environ['OANDA_URL'] = os.getenv('OANDA_URL', 'https://api-fxpractice.oanda.com')
