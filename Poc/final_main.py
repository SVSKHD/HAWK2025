from config import symbols
from logic import ThresholdCalculator
from price_fetcher import fetch_price
from executor import executor
import time
import json

symbol_list = ['EURUSD']

for symbol in symbol_list:
    symbol_data = symbols[symbol]
    start = fetch_price(symbol, "start")

    if start is None:
        print(f"Error: Could not fetch start price for {symbol}")
        continue

    start_price = start["Close_Price"]  # ✅ Fixed Key Name

    while True:
        current = fetch_price(symbol, "current")

        if current is None:
            print(f"Error: Could not fetch current price for {symbol}")
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
            executor(threshold_data)  # ✅ Now Calling Executor

        time.sleep(1)  # ✅ 1-second delay (Consider adjusting)
