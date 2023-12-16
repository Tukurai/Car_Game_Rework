class Position:
    def __init__(self, position: tuple[float, float]):
        self.x = position[0]
        self.y = position[1]

    def get_pos(self) -> tuple[float, float]:
        return (self.x, self.y)
    
    def get_absolute_pos(self):
        return Position(self.get_pos())

    def get_offset_between_pos(self, other):
        """Returns the distance between two positions, used for collision detection"""
        if isinstance(other, Position):
            base = Position(self.get_pos())
            other = Position(other.get_pos())
            return (base.x - other.x, self.y - other.y)
        else:
            raise TypeError("Unsupported variable type for get_offset_between_pos")

    def __add__(self, other) -> tuple[float, float]:
        if isinstance(other, Position):
            base = Position(self.get_pos())
            other = Position(other.get_pos())
            return (base.x + other.x, base.y + other.y)
        else:
            raise TypeError("Unsupported operand type for +")

    def __sub__(self, other) -> tuple[float, float]:
        if isinstance(other, Position):
            base = Position(self.get_pos())
            other = Position(other.get_pos())
            return (base.x - other.x, base.y - other.y)
        else:
            raise TypeError("Unsupported operand type for -")

    def __mul__(self, other) -> tuple[float, float]:
        if isinstance(other, float | int):
            base = Position(self.get_pos())
            return (base.x * other, base.y * other)
        else:
            raise TypeError("Unsupported operand type for *")

    def __truediv__(self, other) -> tuple[float, float]:
        if isinstance(other, float | int):
            base = Position(self.get_pos())
            return (base.x / other, base.y / other)
        else:
            raise TypeError("Unsupported operand type for /")

    def __floordiv__(self, other) -> tuple[float, float]:
        if isinstance(other, float | int):
            base = Position(self.get_pos())
            return (base.x // other, base.y // other)
        else:
            raise TypeError("Unsupported operand type for //")
