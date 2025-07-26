
def classify_regime(candles):
    if len(candles) < 100:
        return 'mixed'
    closes = [c['close'] for c in candles]
    high = max(closes[-20:])
    low = min(closes[-20:])
    mean = sum(closes[-20:]) / 20
    volatility = (high - low) / mean

    recent = closes[-1]
    trend = closes[-1] - closes[-20]

    if trend > 0.002 * mean and volatility > 0.004:
        return 'bull'
    elif trend < -0.002 * mean and volatility > 0.004:
        return 'bear'
    else:
        return 'mixed'
