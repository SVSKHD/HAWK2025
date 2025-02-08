from config import symbols
from logic import ThresholdCalculator
from executor import executor

symbol_list = ['EURUSD']

for symbol in symbol_list:
    symbol_data = symbols[symbol]
    threshold = ThresholdCalculator(symbol, symbol_data['pip'], symbol_data['lot'], symbol_data['threshold'], 1.2000, 1.1955)
    print(threshold.calculate_pip_difference())
    print("="*250)