import json
from notifications import send_notifications  # ✅ Import async function
from trade_management import place_order, close_trades_by_symbol
import MetaTrader5 as mt5

async def executor_notify(data):
    print("Executor received data:")
    print(json.dumps(data, indent=4))  # Pretty print JSON

    # ✅ Accessing threshold hits
    thresholds_hit = data.get("thresholds_hit", {})
    threshold_level = data.get("threshold_level", 0)
    direction = data.get("direction", "neutral")

    # ✅ Conditional clause at the first threshold
    if "1_" in thresholds_hit:
        print(f"🚀 First threshold crossed! ({direction.upper()} Trend Detected)")
        print(f"🔹 Executing action at Threshold 1 for {data['start']} → {data['current']}")

    # ✅ Conditional clause at every subsequent threshold
    for threshold, status in thresholds_hit.items():
        if status:  # Only process if the threshold is hit
            level = int(threshold.split("_")[0])  # Extract threshold level number
            print(f"✅ Threshold {level} crossed ({direction.upper()} Trend)")

            # **Custom Logic for Specific Threshold Levels**
            if level == 1:
                message = f"⚡ First threshold hit at price {data['current']} - Potential entry signal"
                print(message)
                await send_notifications("general", message)  # ✅ Await here
            elif level == 2:
                message = f"📈 Second threshold reached at {data['current']} - Consider adding to position"
                print(message)
                await send_notifications("general", message)  # ✅ Await here
            elif level == 3:
                message = f"🚀 Third threshold hit! Strong momentum at {data['current']}"
                print(message)
                await send_notifications("general", message)  # ✅ Await here
            else:
                print(f"🔥 Higher threshold {level} triggered at {data['current']} - Adjust risk!")

    # ✅ Accessing individual threshold timestamps
    thresholds_hit_time = data.get("thresholds_hit_time", {})

    for threshold, timestamp in thresholds_hit_time.items():
        print(f"Threshold {threshold} was hit at:")
        print(f"  🕒 Server Time: {timestamp['server_time']}")
        print(f"  🇮🇳 IST: {timestamp['IST']}")



async def get_positions(symbol):
    if not mt5.initialize():
        message = "MetaTrader5 initialization failed."
        # await send_discord_message_type(message, "error", True)
        print(message)
        return

    symbol_name = symbol['symbol']
    positions = mt5.positions_get(symbol=symbol_name)
    return positions

# use get positions for all the below operations

# async def execute_trades():
# async def execute_close_trades()
# async def execute_hedging