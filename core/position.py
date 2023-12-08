class Position:
    def __init__(self, position: tuple[float, float]):
        self.x = position[0]
        self.y = position[1]

    def as_tuple(self) -> tuple[float, float]:
        return (self.x, self.y)

    def __add__(self, other) -> tuple[float, float]:
        if isinstance(other, Position):
            return (self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other) -> tuple[float, float]:
        if isinstance(other, Position):
            return (self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported operand type for -")