from datetime import datetime
import pytz

def is_forex_market_open():
    eastern = pytz.timezone('US/Eastern')
    now_eastern = datetime.now(pytz.utc).astimezone(eastern)
    weekday = now_eastern.weekday()  # Monday = 0, Sunday = 6
    hour = now_eastern.hour
    minute = now_eastern.minute

    if weekday == 4 and (hour > 17 or (hour == 17 and minute >= 0)):
        return False  # Friday after 5pm
    elif weekday == 5:  # Saturday
        return False
    elif weekday == 6 and (hour < 17 or (hour == 17 and minute < 0)):
        return False  # Sunday before 5pm
    return True
