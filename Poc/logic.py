from datetime import datetime
import pytz
import json
import math
from decimal import Decimal, ROUND_DOWN

class ThresholdCalculator:
    """
    A class to represent individual symbol data and dynamically calculate threshold levels.
    """

    def __init__(self, symbol, pip, lot, threshold, start, current):
        self.symbol = symbol
        self.pip = Decimal(str(pip))  # Use Decimal for precision
        self.lot = lot
        self.threshold = Decimal(str(threshold))  # Use Decimal for precision
        self.current = Decimal(str(current))  # Use Decimal for precision
        self.start = Decimal(str(start))  # Use Decimal for precision
        self.direction = None
        self.no_thresholds = None

        # Dictionaries to store threshold states (Boolean) and timestamps
        self.thresholds_hit = {}          # Stores Boolean values (True)
        self.thresholds_hit_time = {}     # Stores timestamps (server time & IST)

    def calculate_pip_difference(self):
        # ✅ Use Decimal for high-precision calculation
        difference = self.start - self.current
        formatted_difference = (difference / self.pip).quantize(Decimal('0.01'), rounding=ROUND_DOWN)  # ✅ Fixed precision

        # ✅ Ensure threshold_level never rounds to -1 when below first threshold
        threshold_level = max(0, int(abs(
            (formatted_difference / self.threshold).quantize(Decimal('1.'), rounding=ROUND_DOWN))))

        # Determine direction
        if formatted_difference > 0:
            self.direction = "down"
            threshold_type = "negative"
        elif formatted_difference < 0:
            self.direction = "up"
            threshold_type = "positive"
        else:
            self.direction = "neutral"
            self.no_thresholds = True
            return json.dumps({
                "difference": float(difference),
                "formatted_difference": float(formatted_difference),
                "threshold_level": 0,
                "direction": self.direction,
                "thresholds_hit": {},
                "thresholds_hit_time": {},
                "start": float(self.start),
                "current": float(self.current)
            }, indent=4)

        # Get current timestamps in Server Time (UTC) & Indian Standard Time (IST)
        utc_now = datetime.now(pytz.utc).strftime("%Y-%m-%d %H:%M:%S")
        ist_now = datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")

        # Activate all thresholds leading up to the highest level
        for level in range(1, threshold_level + 1):
            threshold_key = f"{level}_{self.symbol}_{threshold_type}_threshold"
            self.thresholds_hit[threshold_key] = True  # Store Boolean
            self.thresholds_hit_time[threshold_key] = {"server_time": utc_now, "IST": ist_now}  # Store timestamps

        # Convert the final dictionary to a formatted JSON string
        return json.dumps({
            "difference": float(difference),
            "formatted_difference": float(formatted_difference),
            "threshold_level": threshold_level,
            "direction": self.direction,
            "thresholds_hit": self.thresholds_hit,        # Stores Boolean values
            "thresholds_hit_time": self.thresholds_hit_time,  # Stores timestamps
            "start": float(self.start),
            "current": float(self.current)
        }, indent=4)  # Pretty-prints the output
