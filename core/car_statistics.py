from types import SimpleNamespace


class CarStatistics:
    """Class for storing a car's statistics, previous and current."""

    def __init__(self):
        self.current = SimpleNamespace(tolerance=0, speed=0, rotation=0)
        self.previous = None
    
    def update(self):
        """Update the statistics."""
        self.previous = self.current