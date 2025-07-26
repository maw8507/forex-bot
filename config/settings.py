import os

def load_config():
    os.environ['OANDA_API_KEY'] = os.getenv('OANDA_API_KEY', 'your-api-key')
    os.environ['OANDA_ACCOUNT_ID'] = os.getenv('OANDA_ACCOUNT_ID', 'your-account-id')
    os.environ['OANDA_URL'] = os.getenv('OANDA_URL', 'https://api-fxpractice.oanda.com')

def get_settings():
    return {
        'OANDA_API_KEY': os.getenv('OANDA_API_KEY'),
        'OANDA_ACCOUNT_ID': os.getenv('OANDA_ACCOUNT_ID'),
        'OANDA_URL': os.getenv('OANDA_URL'),
        'OANDA_ENVIRONMENT': os.getenv('OANDA_ENVIRONMENT', 'practice'),
    }
