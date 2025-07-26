
from utils.logger import logger
from logic.capital_allocator import allocate_capital

class TradeExecutor:
    def execute_trade(self, signal, portfolio):
        position = portfolio.get_position(signal['pair'])
        capital = allocate_capital(signal, portfolio)

        if signal['action'] == 'buy':
            if position and position['side'] == 'long':
                logger.info(f"Already in long {signal['pair']}")
            else:
                logger.info(f"Placing LONG order for {signal['pair']} with ${capital:.2f}")
                portfolio.open_position(signal['pair'], 'long', capital, signal['confidence'])

        elif signal['action'] == 'sell':
            if position and position['side'] == 'short':
                logger.info(f"Already in short {signal['pair']}")
            else:
                logger.info(f"Placing SHORT order for {signal['pair']} with ${capital:.2f}")
                portfolio.open_position(signal['pair'], 'short', capital, signal['confidence'])

        elif signal['action'] == 'close':
            if position:
                logger.info(f"Closing position on {signal['pair']}")
                portfolio.close_position(signal['pair'])
