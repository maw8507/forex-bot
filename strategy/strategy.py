
class Strategy:
    def generate_signals(self, pair, tf, candles, regime):
        if len(candles) < 100:
            return []

        close_prices = [c['close'] for c in candles]
        sma_fast = sum(close_prices[-10:]) / 10
        sma_slow = sum(close_prices[-50:]) / 50

        signal = None
        if regime == 'bull':
            if sma_fast > sma_slow:
                signal = {'pair': pair, 'action': 'buy', 'confidence': 0.8}
            elif sma_fast < sma_slow:
                signal = {'pair': pair, 'action': 'close', 'confidence': 0.7}
        elif regime == 'bear':
            if sma_fast < sma_slow:
                signal = {'pair': pair, 'action': 'sell', 'confidence': 0.85}
            elif sma_fast > sma_slow:
                signal = {'pair': pair, 'action': 'close', 'confidence': 0.7}
        else:
            if abs(sma_fast - sma_slow) / sma_slow < 0.002:
                signal = {'pair': pair, 'action': 'buy', 'confidence': 0.6}
            else:
                signal = {'pair': pair, 'action': 'close', 'confidence': 0.5}

        return [signal] if signal else []
