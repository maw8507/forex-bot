
class PortfolioManager:
    def __init__(self):
        self.total_equity = 1000
        self.positions = {}
        self.trading_pairs = {
            'EUR_USD': ['M15', 'H1'],
            'GBP_USD': ['H1'],
            'USD_JPY': ['M15'],
            'USD_ZAR': ['H1'],
            'USD_MXN': ['H1']
        }

    def get_position(self, pair):
        return self.positions.get(pair)

    def open_position(self, pair, side, capital, confidence):
        self.positions[pair] = {
            'side': side,
            'capital': capital,
            'confidence': confidence
        }

    def close_position(self, pair):
        if pair in self.positions:
            del self.positions[pair]
