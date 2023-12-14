from core.sprites.sprite import Sprite


class CarProperties:
    """Class for storing car properties such as max speed, acceleration, handling, drag, etc."""

    def __init__(self, max_speed: int, acceleration: int, handling: int, drag: int, tolerance: int, braking: int):
        self.max_speed = max_speed
        self.acceleration = acceleration
        self.handling = handling
        self.drag = drag
        self.tolerance = tolerance
        self.braking = braking