from config import symbols
from logic import ThresholdCalculator

symbols_list = ['EURUSD']
prices = [1.2015, 1.2030, 1.2045]
negative_prices = [1.1985, 1.1970, 1.1955]
for symbol in symbols_list:
    symbol_data = symbols[symbol]  # Get the full dictionary for the symbol
    # Pass all necessary values to the ThresholdCalculator
    for price in negative_prices:
        threshold = ThresholdCalculator(symbols[symbol], symbol_data['pip'], symbol_data['lot'], symbol_data['threshold'], 1.2000, price)
        print(threshold.calculate_pip_difference())
        print("="*250)