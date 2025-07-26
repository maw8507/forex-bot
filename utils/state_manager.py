
import time

_last_fetch_time = {}

def should_fetch_candles(pair, tf, interval_sec=60):
    key = f"{pair}:{tf}"
    now = time.time()
    last = _last_fetch_time.get(key, 0)
    return (now - last) > interval_sec

def update_last_fetch_time(pair, tf):
    key = f"{pair}:{tf}"
    _last_fetch_time[key] = time.time()
