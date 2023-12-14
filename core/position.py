class Position:
    def __init__(self, position: tuple[float, float]):
        self.x = position[0]
        self.y = position[1]

    def get_pos(self) -> tuple[float, float]:
        return (self.x, self.y)

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