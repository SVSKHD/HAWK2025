import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pytz

# Define timeframe
TIMEFRAME = mt5.TIMEFRAME_M5


def fetch_price(symbol, time_type="start"):
    if not mt5.initialize():
        print("MT5 initialization failed")
        quit()

    server_timezone = pytz.timezone("Etc/UTC")

    if time_type == "start":
        today = datetime.now(server_timezone).date()

        # If today is Monday, Sunday, or Saturday → Get Friday 11:45 PM (23:45)
        if today.weekday() in [0, 5, 6]:  # Monday (0), Saturday (5), Sunday (6)
            last_friday = today - timedelta(days=(today.weekday() + 2) % 7 + 1)
            time_to_fetch = datetime(last_friday.year, last_friday.month, last_friday.day, 23, 55, 0, tzinfo=server_timezone)
        else:
            # Other days → Get 12 AM (00:00)
            time_to_fetch = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=server_timezone)

    elif time_type == "current":
        # Get the latest available price
        time_to_fetch = datetime.now(server_timezone)
    else:
        print("Invalid argument. Use 'start' for 12 AM/11:45 PM price or 'current' for current price.")
        return None

    # Fetch the price data
    rates = mt5.copy_rates_from(symbol, TIMEFRAME, time_to_fetch, 1)

    if rates is None or len(rates) == 0:
        print(f"No data retrieved for {time_type} price. Check symbol and timeframe.")
        return None

    # Extract candle data
    candle = rates[0]
    return {
        "Open": candle['open'],
        "High": candle['high'],
        "Low": candle['low'],
        "Close": candle['close'],
        "Time": datetime.fromtimestamp(candle['time'], server_timezone)
    }


# Fetch adjusted 12 AM or 11:45 PM price
price_12am = fetch_price("EURUSD", "start")
if price_12am:
    print(f"Price on {price_12am['Time']}: {price_12am['Close']}")

# Fetch current price
current_price = fetch_price("EURUSD", "current")
if current_price:
    print(f"Current Price at {current_price['Time']}: {current_price['Close']}")

# Shutdown MT5
mt5.shutdown()
