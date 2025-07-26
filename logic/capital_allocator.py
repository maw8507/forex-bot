
def allocate_capital(signal, portfolio):
    base = portfolio.total_equity
    confidence = signal['confidence']
    return min(base * confidence / 2.0, base)  # soft max capital cap
