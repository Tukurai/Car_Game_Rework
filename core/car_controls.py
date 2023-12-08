from core.enums.direction import Direction


class CarControls:
    """Class for storing car controls."""

    def __init__(self, mapping: dict[Direction, int]):
        self.__mapping = mapping
        self.__revese_mapping = {v: k for k, v in mapping.items()}

    def get_key(self, direction: Direction) -> int:
        """Return the key for the given direction."""
        return self.__mapping[direction]
    
    def get_direction(self, key: int) -> Direction:
        """Return the direction for the given key."""
        return self.__revese_mapping[key]