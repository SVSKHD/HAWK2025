import MetaTrader5 as mt5
from datetime import datetime, timedelta
import pytz
import asyncio
from concurrent.futures import ThreadPoolExecutor

# Define timeframe
TIMEFRAME = mt5.TIMEFRAME_M5

# Create a thread pool executor for MT5 functions
executor = ThreadPoolExecutor(max_workers=2)

async def fetch_price(symbol, time_type="start"):
    """Async function to fetch price data from MetaTrader 5 (MT5)."""

    loop = asyncio.get_running_loop()

    # Run the synchronous MT5 function in a separate thread
    return await loop.run_in_executor(executor, _sync_fetch_price, symbol, time_type)

def _sync_fetch_price(symbol, time_type):
    """Synchronous function to fetch price data from MT5 (Runs in a separate thread)."""

    if not mt5.initialize():
        print("❌ MT5 initialization failed")
        return None

    server_timezone = pytz.timezone("Etc/UTC")

    if time_type == "start":
        today = datetime.now(server_timezone).date()

        # If today is Monday, Sunday, or Saturday → Get Friday 11:55 PM (23:55)
        if today.weekday() in [0, 5, 6]:  # Monday (0), Saturday (5), Sunday (6)
            last_friday = today - timedelta(days=(today.weekday() + 2) % 7 + 1)
            time_to_fetch = datetime(last_friday.year, last_friday.month, last_friday.day, 23, 55, 0, tzinfo=server_timezone)
        else:
            # Other days → Get 12 AM (00:00)
            time_to_fetch = datetime(today.year, today.month, today.day, 0, 0, 0, tzinfo=server_timezone)

        # Fetch the historical price data
        rates = mt5.copy_rates_from(symbol, TIMEFRAME, time_to_fetch, 1)

        if rates is None or len(rates) == 0:
            print(f"❌ No data retrieved for {time_type} price. Check symbol and timeframe.")
            return None

        # Extract and return Close price
        candle = rates[0]
        return {
            "Symbol": symbol,
            "Time": datetime.fromtimestamp(candle['time'], server_timezone),
            "Close_Price": candle['close']  # ✅ Returning Close price
        }

    elif time_type == "current":
        # ✅ Fetch real-time tick data
        tick = mt5.symbol_info_tick(symbol)

        if tick is None:
            print(f"❌ No tick data retrieved for {symbol}. Market might be closed.")
            return None

        # Extract and return Bid price
        return {
            "Symbol": symbol,
            "Time": datetime.fromtimestamp(tick.time, server_timezone),
            "Bid_Price": tick.bid  # ✅ Returning Bid price
        }

    else:
        print("❌ Invalid argument. Use 'start' for 12 AM/11:55 PM price or 'current' for real-time price.")
        return None

