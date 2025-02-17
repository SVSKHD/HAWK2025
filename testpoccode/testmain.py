import ntplib
import asyncio
from datetime import datetime
import pytz

NTP_SERVERS = ["time.google.com", "time.windows.com", "time.apple.com", "pool.ntp.org"]

TIME_CHECK = "10:00:00"  # Target time to check

async def get_ntp_time():
    """Fetches UTC time from NTP servers, with a fallback to system time if all fail."""
    for server in NTP_SERVERS:
        try:
            client = ntplib.NTPClient()
            response = client.request(server, version=3)
            utc_time = datetime.utcfromtimestamp(response.tx_time)
            return utc_time
        except Exception:
            pass  # Silently fail and try the next server

    print("⚠ All NTP servers failed! Using local system time.")
    return datetime.utcnow()

async def display_time():
    """Continuously fetches and prints GMT+2 time in real-time."""
    gmt_plus_2 = pytz.timezone('Etc/GMT-2')

    while True:
        utc_time = await get_ntp_time()
        server_time = utc_time.replace(tzinfo=pytz.utc).astimezone(gmt_plus_2)

        # Print server time
        print(f"\r⏳ Server Time (GMT+2): {server_time.strftime('%Y-%m-%d %H:%M:%S')}", end='', flush=True)

        # Check if the current time matches the target time
        if server_time.strftime('%H:%M:%S') == TIME_CHECK:
            print(f"\n📢 Time Matched: {server_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
            break  # Stop checking once the time matches

        await asyncio.sleep(1)  # Refresh every second for accuracy

# Run the async event loop
print("⏳ Waiting for the target time...")
asyncio.run(display_time())
