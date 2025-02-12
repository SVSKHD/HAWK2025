from config import symbols
from logic import ThresholdCalculator
from price_fetcher import fetch_price
from executor import executor  # ✅ Import async executor
import asyncio
import json
from datetime import datetime, timezone, timedelta


symbol_list = ['EURUSD']

async def process_symbol(symbol):
    """Async function to fetch price and calculate thresholds with auto-reset at 12 AM."""
    symbol_data = symbols[symbol]

    # ✅ Fetch initial start price
    start = await fetch_price(symbol, "start")

    if start is None:
        print(f"❌ Error: Could not fetch start price for {symbol}")
        return

    start_price = start["Close_Price"]  # ✅ Fixed Key Name

    # ✅ Keep track of the last fetched date
    last_reset_date = datetime.now(timezone.utc).date()
    # test code
    # last_reset_date = datetime.now(timezone.utc).date() - timedelta(days=1)  # ✅ Force immediate reset

    while True:
        # ✅ Get current UTC time
        current_utc_time = datetime.now(timezone.utc)

        # ✅ Check if a new day has started (12 AM UTC)
        if current_utc_time.date() > last_reset_date:
            print(f"🔄 Resetting start price for {symbol} at 12 AM UTC...")
            new_start = await fetch_price(symbol, "start")  # Fetch new start price

            if new_start:
                start_price = new_start["Close_Price"]  # ✅ Update start price
                last_reset_date = current_utc_time.date()  # ✅ Update last reset date
                print(f"✅ New start price for {symbol}: {start_price}")

        # ✅ Fetch the current price
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
            await executor(threshold_data)  # ✅ Await async executor

        await asyncio.sleep(1)  # ✅ Use asyncio.sleep instead of time.sleep

async def main():
    """Run all symbols asynchronously."""
    tasks = [process_symbol(symbol) for symbol in symbol_list]
    await asyncio.gather(*tasks)

# Run the async event loop
if __name__ == "__main__":
    asyncio.run(main())  # ✅ Run async main
