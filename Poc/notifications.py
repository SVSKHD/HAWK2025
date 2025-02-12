import aiohttp
import asyncio
from dynaconf import Dynaconf

# Load settings from settings.toml
settings = Dynaconf(settings_files=["settings.toml"], environments=True)

# Get Discord webhook URLs from settings
hawk_trade = settings.hawk_trade
hawk_general = settings.hawk_general


async def send_notifications(channel_type, message):
    """Send notification to the appropriate Discord channel."""

    # ✅ Choose the correct webhook URL
    url = hawk_trade if channel_type == "trade" else hawk_general

    if not url:
        print(f"❌ Error: No URL configured for {channel_type}")
        return

    payload = {"content": message}  # Discord expects 'content' in JSON format

    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=payload) as response:
            if response.status == 204:
                print(f"✅ Message sent successfully to {channel_type} channel.")
            else:
                print(f"❌ Failed to send message: {response.status}")

