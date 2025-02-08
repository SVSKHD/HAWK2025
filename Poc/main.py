from logic import ThresholdCalculator
# Example with EURUSD (Crossing 2 thresholds)
calculator1 = ThresholdCalculator("EURUSD", 0.0001, 1, 15, 1.1000, 1.1010)
result1 = calculator1.calculate_pip_difference()
print(result1)

# # Example with GBPUSD (Crossing 3 thresholds)
# calculator2 = ThresholdCalculator("GBPUSD", 0.0001, 1, 10, 1.3000, 1.3055)
# result2 = calculator2.calculate_pip_difference()
# print(result2)
