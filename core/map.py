from argparse import FileType
from core.car import Car
from core.enums.direction import Direction

from core.position import Position
from core.enums.sprite_type import SpriteType

from settings import Settings


class Map:
    """Map class, used to store the map data and the map objects. This is what a player races on."""

    def __init__(self, name: str, ground, road, objects, checkpoints) -> None:
        self.name = name
        self.ground = ground
        self.road = road
        self.objects = objects
        self.checkpoints = checkpoints

    def get_start_positions(self, amount: int) -> list[tuple[Position, Direction]]:
        """Get the starting positions for an amount players."""

        centerpoint = self.checkpoints[0] + Position(
            (Settings.TILE_SIZE // 2, Settings.TILE_SIZE // 2)
        )
        direction = self.get_direction(self.checkpoints[0], self.checkpoints[1])

        # offset the starting positions to be behind the start line
        offset_values = {
            Direction.UP: (0, 40),
            Direction.DOWN: (0, -40),
            Direction.LEFT: (40, 0),
            Direction.RIGHT: (-40, 0),
        }
        centerpoint += (
            Position(offset_values[direction]) * Settings.SCALE[SpriteType.GLOBAL]
        )

        # set starting positions
        for index in range(amount):
            pair_index = index % 2
            row_index = index // 2
            pair_offset = 50
            row_offset = 140 * Settings.SCALE[SpriteType.VEHICLE]

            starting_position = Position(centerpoint)

            if direction in (Direction.UP, Direction.DOWN):
                starting_position.x += pair_offset if pair_index else -pair_offset
                starting_position.y += (
                    row_offset * row_index
                    if direction == Direction.UP
                    else -row_offset * row_index
                )
            else:  # Direction.LEFT, Direction.RIGHT
                starting_position.x += (
                    row_offset * row_index
                    if direction == Direction.LEFT
                    else -row_offset * row_index
                )
                starting_position.y += pair_offset if pair_index else -pair_offset

            # Offset the car based on the direction
            car_offset_values = {
                Direction.UP: (8, -18),
                Direction.DOWN: (8, -18),
                Direction.LEFT: (3, 8),
                Direction.RIGHT: (-18, 8),
            }
            starting_position += Position(car_offset_values[direction])

            yield (index, starting_position, direction)

    def get_direction(self, checkpoint_a: Position, checkpoint_b: Position):
        """Get the direction between the two provided checkpoints."""
        x1, y1 = checkpoint_a.get_pos()
        x2, y2 = checkpoint_b.get_pos()

        return {
            (x1 < x2): Direction.RIGHT,
            (x1 > x2): Direction.LEFT,
            (y1 < y2): Direction.DOWN,
            (y1 > y2): Direction.UP,
        }[True]
    
    def handle_event(self, event):
        """Handle any non pygame.QUIT event."""
        return
    
    def update(self, timedelta, input_state):
        """Update the component and all its children"""
        return

    def draw(self, screen, opacity: int = 255):
        """Draw the map."""
        for tile in self.ground:
            tile.draw(screen, opacity)

        for tile in self.road:
            tile.draw(screen, opacity)

        for tile in self.objects:
            tile.draw(screen, opacity)
