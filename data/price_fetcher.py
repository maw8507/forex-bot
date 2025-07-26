
import os
import requests
from utils.logger import logger

class OandaPriceFetcher:
    def __init__(self):
        self.api_key = os.environ['OANDA_API_KEY']
        self.account_id = os.environ['OANDA_ACCOUNT_ID']
        self.base_url = os.environ['OANDA_URL']
        self.headers = {
            "Authorization": f"Bearer {self.api_key}"
        }

    def get_candle_data(self, pair, granularity, count=1):
        url = f"{self.base_url}/v3/instruments/{pair}/candles"
        params = {
            "granularity": granularity,
            "count": count,
            "price": "M"
        }
        response = requests.get(url, headers=self.headers, params=params)
        if response.status_code != 200:
            logger.error(f"Failed to fetch candles: {response.text}")
            return []
        data = response.json()
        return [{
            "time": c["time"],
            "open": float(c["mid"]["o"]),
            "high": float(c["mid"]["h"]),
            "low": float(c["mid"]["l"]),
            "close": float(c["mid"]["c"]),
            "volume": int(c["volume"])
        } for c in data["candles"] if c["complete"]]
