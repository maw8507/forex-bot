import os
import requests
from utils.logger import logger
from logic.capital_allocator import allocate_capital

class TradeExecutor:
    def __init__(self):
        self.account_id = os.getenv("OANDA_ACCOUNT_ID")
        self.api_key = os.getenv("OANDA_API_KEY")
        env = os.getenv("OANDA_ENVIRONMENT", "practice").lower()
        self.base_url = (
            "https://api-fxpractice.oanda.com/v3"
            if env == "practice"
            else "https://api-fxtrade.oanda.com/v3"
        )
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def execute_trade(self, signal, portfolio):
        position = portfolio.get_position(signal["pair"])
        capital = allocate_capital(signal, portfolio)
        instrument = signal["pair"]

        if signal["action"] == "buy":
            if position and position["side"] == "long":
                logger.info(f"Already in long {signal['pair']}")
            else:
                logger.info(f"Sending LONG order to OANDA for {signal['pair']} with ${capital:.2f}")
                self._place_order(instrument, capital, "buy")

        elif signal["action"] == "sell":
            if position and position["side"] == "short":
                logger.info(f"Already in short {signal['pair']}")
            else:
                logger.info(f"Sending SHORT order to OANDA for {signal['pair']} with ${capital:.2f}")
                self._place_order(instrument, capital, "sell")

        elif signal["action"] == "close":
            if position:
                logger.info(f"Closing position on {signal['pair']}")
                self._close_position(instrument)
                portfolio.close_position(signal["pair"])

    def _place_order(self, instrument, usd_amount, side):
        units = self._calculate_units(instrument, usd_amount, side)
        if not units:
            logger.warning(f"Unable to calculate units for {instrument}")
            return

        order_data = {
            "order": {
                "units": units,
                "instrument": instrument,
                "timeInForce": "FOK",
                "type": "MARKET",
                "positionFill": "DEFAULT"
            }
        }

        url = f"{self.base_url}/accounts/{self.account_id}/orders"
        response = requests.post(url, json=order_data, headers=self.headers)

        if response.status_code == 201:
            logger.info(f"Trade executed for {instrument}: {side.upper()} {units} units")
        else:
            logger.error(f"Order failed: {response.status_code} {response.text}")

    def _calculate_units(self, instrument, usd_amount, side):
        try:
            price_url = f"{self.base_url}/instruments/{instrument}/pricing"
            params = {"instruments": instrument}
            r = requests.get(price_url, headers=self.headers, params=params)
            r.raise_for_status()
            price = float(r.json()["prices"][0]["asks"][0]["price"])
            units = int(usd_amount / price)
            return str(units if side == "buy" else -units)
        except Exception as e:
            logger.error(f"Failed to get price for {instrument}: {e}")
            return None

    def _close_position(self, instrument):
        try:
            url = f"{self.base_url}/accounts/{self.account_id}/positions/{instrument}/close"
            requests.put(url, headers=self.headers, json={"longUnits": "ALL", "shortUnits": "ALL"})
        except Exception as e:
            logger.error(f"Failed to close position on {instrument}: {e}")
