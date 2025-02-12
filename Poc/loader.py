import toml

# Load settings from `settings.toml`
def load_settings():
    try:
        with open("settings.toml", "r") as file:
            settings = toml.load(file)
            return settings
    except Exception as e:
        print(f"Error loading settings: {e}")
        return {}

# Store the settings globally
SETTINGS = load_settings()

# ✅ Make settings accessible from other files
def get_setting(key, default=None):
    keys = key.split(".")
    value = SETTINGS
    for k in keys:
        value = value.get(k, default) if isinstance(value, dict) else default
    return value
