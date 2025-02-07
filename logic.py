class ThresholdCalculator:
    """
    A class to represent individual symbol data.
    """

    def __init__(self, symbol, pip, lot, threshold, start, current):
        self.second_positive_threshold = None
        self.second_negative_threshold = None
        self.first_positive_threshold = None
        self.first_negative_threshold = None
        self.direction = None
        self.no_thresholds = None
        self.symbol = symbol
        self.pip = pip
        self.lot = lot
        self.threshold = threshold
        self.current = current
        self.start = start
        self.second_threshold_limit = 2 * self.threshold

    def calculate_pip_difference(self):
        difference = self.start - self.current
        formatted_difference = difference / self.pip
        threshold = round(formatted_difference / self.threshold,2)

        # Check second threshold first
        if threshold >= 2:
            self.direction = "down"
            self.second_negative_threshold = True
            self.first_negative_threshold = True
        elif threshold <= -2:
            self.direction = "up"
            self.second_positive_threshold = True
            self.first_positive_threshold = True
        elif threshold >= 1:
            self.direction = "down"
            self.first_negative_threshold = True
        elif threshold <= -1:
            self.direction = "up"
            self.first_positive_threshold = True
        else:  # Covers the range -1 < threshold < 1 (including 0)
            self.direction = "neutral"
            self.no_thresholds = True

        return {
            "difference": difference,
            "formatted_difference": formatted_difference,
            "first_positive": self.first_positive_threshold,
            "first_negative": self.first_negative_threshold,
            "second_positive": self.second_positive_threshold,
            "second_negative": self.second_negative_threshold,
            "threshold": threshold,
            "direction": self.direction,
            "start": self.start,
            "current": self.current
        }