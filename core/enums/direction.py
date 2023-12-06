from enum import Enum


class Direction(Enum):
    """Enum for directions, used by the Car class, also used to determine directions for the AI."""

    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
