from logic import ThresholdCalculator
import json  # Import json module for handling JSON strings

# Example with EURUSD (Crossing 2 thresholds)
calculator1 = ThresholdCalculator("EURUSD", 0.0001, 1, 15, 1.1000, 1.1030)
result1 = calculator1.calculate_pip_difference()

# Check if result1 is a JSON string or dictionary
if isinstance(result1, str):
    result1 = json.loads(result1)  # Convert JSON string to dictionary if needed

# Print the full result
print("Full Result:")
print(json.dumps(result1, indent=4))  # Pretty-print the JSON

# Access only the 'thresholds_hit' object
print("\nThresholds Hit:")
print(result1["thresholds_hit"])
