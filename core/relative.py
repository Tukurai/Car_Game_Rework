from core.position import Position


class Relative(Position):
    def __init__(self, relative_pos: Position, offset: tuple[float, float]):
        super().__init__(offset)
        self.relative_pos = relative_pos

    def get_pos(self) -> tuple[float, float]:
        return self.relative_pos.get_pos() + super()
