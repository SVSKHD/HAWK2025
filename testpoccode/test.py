import MetaTrader5 as mt5
from datetime import datetime, timezone, timedelta
import pytz

# Display MetaTrader5 package info
print("MetaTrader5 package author:", mt5.__author__)
print("MetaTrader5 package version:", mt5.__version__)

# Establish connection to the MetaTrader 5 terminal
if not mt5.initialize():
    print("initialize() failed, error code =", mt5.last_error())
    quit()

# Attempt to enable GBPUSD in MarketWatch
selected = mt5.symbol_select("GBPUSD", True)
if not selected:
    print("Failed to select GBPUSD")
    mt5.shutdown()
    quit()

# Get the last tick for GBPUSD
lasttick = mt5.symbol_info_tick("GBPUSD")
if lasttick is None:
    print("Failed to retrieve tick data")
    mt5.shutdown()
    quit()

# Convert server time to UTC
server_time_utc = datetime.utcfromtimestamp(lasttick.time).replace(tzinfo=timezone.utc)
server_time_msc_utc = datetime.utcfromtimestamp(lasttick.time_msc / 1000).replace(tzinfo=timezone.utc)

# Get local time with timezone info
local_time = datetime.now().astimezone()

# Calculate timezone offset
time_difference_hours = round((server_time_utc - datetime.now(timezone.utc)).total_seconds() / 3600, 2)

# Manually list UTC-2 time zones (since they are rare)
utc_minus_2_zones = [
    "America/Noronha",  # Brazil
    "Atlantic/South_Georgia",  # South Georgia and the South Sandwich Islands
    "Etc/GMT-2"  # Generic UTC-2
]

# Try to match a timezone
possible_timezones = [tz for tz in pytz.all_timezones if datetime.now(pytz.timezone(tz)).utcoffset() == timedelta(hours=time_difference_hours)]
if not possible_timezones and time_difference_hours == -2:
    possible_timezones = utc_minus_2_zones

# Print times for comparison
print("\nTime Comparison:")
print(f"Server Time (UTC): {server_time_utc.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Server Time with Milliseconds (UTC): {server_time_msc_utc.strftime('%Y-%m-%d %H:%M:%S.%f')}")
print(f"Local Time: {local_time.strftime('%Y-%m-%d %H:%M:%S.%f %Z')}")
print(f"Broker Timezone Offset from UTC: {time_difference_hours:.2f} hours")

# Print identified timezone
if possible_timezones:
    print(f"Possible Broker Timezones: {possible_timezones}")
else:
    print("Broker Timezone: Could not determine an exact match.")

# Shut down connection to MetaTrader 5 terminal
mt5.shutdown()
