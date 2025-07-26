
import time
from collections import defaultdict, deque
from config.settings import load_config
from data.price_fetcher import OandaPriceFetcher
from execution.trade_executor import TradeExecutor
from portfolio.portfolio_manager import PortfolioManager
from strategy.strategy_engine import StrategyEngine
from utils.logger import logger
from utils.state_manager import should_fetch_candles, update_last_fetch_time

load_config()
price_fetcher = OandaPriceFetcher()
portfolio = PortfolioManager()
executor = TradeExecutor()
strategy_engine = StrategyEngine()

CANDLE_LOOKBACK = 300
candle_buffer = defaultdict(lambda: deque(maxlen=CANDLE_LOOKBACK))

def preload_history():
    logger.info("Preloading historical candles...")
    for pair, timeframes in portfolio.trading_pairs.items():
        for tf in timeframes:
            try:
                candles = price_fetcher.get_candle_data(pair, tf, count=CANDLE_LOOKBACK)
                key = f"{pair}:{tf}"
                candle_buffer[key].extend(candles)
                update_last_fetch_time(pair, tf)
                logger.info(f"Loaded {len(candles)} candles for {pair} {tf}")
            except Exception as e:
                logger.error(f"Preload failed for {pair} {tf}: {e}")

def run_live_trading():
    logger.info("Starting live trading...")
    preload_history()
    while True:
        for pair, timeframes in portfolio.trading_pairs.items():
            for tf in timeframes:
                if not should_fetch_candles(pair, tf):
                    continue
                try:
                    new_candles = price_fetcher.get_candle_data(pair, tf, count=1)
                    if not new_candles:
                        continue
                    key = f"{pair}:{tf}"
                    candle_buffer[key].extend(new_candles)
                    update_last_fetch_time(pair, tf)
                    candles = list(candle_buffer[key])
                    signals = strategy_engine.generate_signals(pair, tf, candles)
                    for signal in signals:
                        executor.execute_trade(signal, portfolio)
                except Exception as e:
                    logger.exception(f"Processing error {pair} {tf}: {e}")
        time.sleep(10)

if __name__ == "__main__":
    try:
        run_live_trading()
    except KeyboardInterrupt:
        logger.info("Bot shutdown requested.")
