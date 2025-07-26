
from strategy.strategy import Strategy
from logic.regime_classifier import classify_regime
from utils.logger import logger

class StrategyEngine:
    def __init__(self):
        self.strategy = Strategy()

    def generate_signals(self, pair, timeframe, candles):
        try:
            regime = classify_regime(candles)
            return self.strategy.generate_signals(pair, timeframe, candles, regime)
        except Exception as e:
            logger.error(f"Strategy error for {pair} {timeframe}: {e}")
            return []
