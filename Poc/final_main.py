from HAWK2025.Poc.notifications import send_notifications
from config import symbols
from logic import ThresholdCalculator
from price_fetcher import fetch_price
from executor import executor_notify  # ✅ Import async executor
import asyncio
import json
from datetime import datetime, timezone, timedelta
import pytz

symbol_list = ['EURUSD']
START_RESET = "00:00:00"  # ✅ Reset time in UTC
SERVER_TIMEZONE = pytz.timezone("Etc/GMT-2")  # ✅ Define server timezone (GMT+2)


async def process_symbol(symbol):
    symbol_data = symbols[symbol]

    # ✅ Fetch initial start price
    start = await fetch_price(symbol, "start")

    if start is None:
        print(f"❌ Error: Could not fetch start price for {symbol}")
        return

    start_price = start["Close_Price"]  # ✅ Fixed Key Name

    # ✅ Keep track of the last fetched date
    last_reset_date = datetime.now(timezone.utc).date()

    while True:
        # ✅ Get current UTC time
        current_utc_time = datetime.now(timezone.utc)
        server_time_obj = datetime.now(SERVER_TIMEZONE)
        server_time_str = server_time_obj.strftime("%Y-%m-%d %H:%M:%S")

        print(f"🕒 Server Time (GMT+2): {server_time_str}")

        # ✅ Check if it's exactly 19:57:00 GMT+2
        if server_time_obj.strftime("%H:%M:%S") == START_RESET:
            print(f"🔔 [ALERT] It's {START_RESET} GMT+2! Resetting start price for {symbol}...")
            new_start = await fetch_price(symbol, "start")  # Fetch new start price
            message = f"🔔 [ALERT] It's {START_RESET} GMT+2! Resetting start price for {symbol}... {new_start['Close_Price']}"
            await send_notifications("trade", message=message)  # ✅ Await here

            if new_start:
                start_price = new_start["Close_Price"]  # ✅ Update start price
                last_reset_date = current_utc_time.date()  # ✅ Update last reset date
                print(f"✅ [UPDATED] New start price for {symbol}: {start_price}")
            else:
                print(f"⚠️ [WARNING] Failed to fetch new start price at 19:57:00 GMT+2.")

        # ✅ Fetch the current price
        print(f"🔄 Fetching latest price for {symbol}...")
        current = await fetch_price(symbol, "current")

        if current is None:
            print(f"❌ Error: Could not fetch current price for {symbol}")
            continue

        current_price = current['Bid_Price']

        threshold = ThresholdCalculator(
            symbol, symbol_data['pip'], symbol_data['lot'], symbol_data['threshold'], start_price, current_price
        )

        threshold_data = json.loads(threshold.calculate_pip_difference())  # Convert JSON to Dictionary
        print(json.dumps(threshold_data, indent=4))
        print("=" * 100)

        # 🚀 **Trigger Executor if Threshold Hit**
        if threshold_data["thresholds_hit"]:
            await executor_notify(threshold_data)  # ✅ Await async executor

        await asyncio.sleep(1)  # ✅ Use asyncio.sleep instead of time.sleep


async def main():
    """Run all symbols asynchronously."""
    tasks = [process_symbol(symbol) for symbol in symbol_list]
    await asyncio.gather(*tasks)  # ✅ Run all symbol processing tasks


# Run the async event loop
if __name__ == "__main__":
    asyncio.run(main())  # ✅ Run async main
