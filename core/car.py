import math
from types import SimpleNamespace

import pygame
from core.car_properties import CarProperties
from core.car_statistics import CarStatistics
from core.enums.direction import Direction
from core.event_handler import EventHandler
from core.input_state import InputState
from core.position import Position
from core.relative import Relative
from core.sprites.sprite import Sprite


class Car:
    """Class for handeling a Car."""

    def __init__(
        self, name: str, sprite: Sprite, position: Position, properties: CarProperties
    ):
        self.name = name
        self.sprite = sprite

        self.position = position
        self.previous_position = None

        self.properties = properties
        self.statistics = CarStatistics()

        self.score = 0
        self.lap = 0
        self.penalties = 0
        self.place = 0

        self.sprite.position = Relative(self.position, (0, 0))

        # Create events
        self.events = SimpleNamespace()
        self.events.on_car_driving = EventHandler()
        self.events.on_car_reset = EventHandler()

    def set_position(self, position: Position):
        """Set the position of the car, also altering the sprite position relatively.
        Replacing the position property will not alter the sprite position."""
        self.position.x = position.x
        self.position.y = position.y

    def set_rotation(self, rotation: float):
        """Set the rotation of the car, also altering the sprite rotation relatively.
        Replacing the rotation property will not alter the sprite rotation."""
        self.statistics.current.rotation = rotation
        self.sprite.rotation = rotation

    def get_size(self) -> tuple[int, int]:
        """Return the size of the car after applying scale."""
        return (int(self.__size * self.__scale), int(self.__size * self.__scale))

    def update(self, delta_time: float, input_state: InputState):
        """Update the car."""

        # Update the car statistics
        self.statistics.update()

    def draw(self, screen, opacity: int = 255):
        """Draw the car."""
        # Draw the car
        self.sprite.draw(screen, opacity)

        # Draw the name
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        text_outline = font.render(self.name, True, (0, 0, 0))

        centered_x = (
            self.position.get_pos()[0]
            + (self.sprite.get_scaled_size()[0] / 2)
            - (text.get_width() / 2)
        )
        centered_y = (
            self.position.get_pos()[1]
            + (self.sprite.get_scaled_size()[1] / 2)
            - (text.get_height() / 2)
        )

        tag_offset_y = 50

        for x_offset in [-1, 1]:
            for y_offset in [-1, 1]:
                screen.blit(
                    text_outline,
                    (centered_x + x_offset, centered_y + y_offset - tag_offset_y),
                )

        screen.blit(text, (centered_x, centered_y - tag_offset_y))

    def handle_event(self, event):
        """Handle any non pygame.QUIT event."""
        return

    def apply_drag(self):
        """Apply drag to the car, decreasing the speed."""
        speed = self.statistics.current.speed
        drag = self.properties.drag

        self.statistics.current.speed = speed - drag if speed > 0 else speed + drag

    def speed_limiter(self, speed_mod: int) -> int:
        """Limit the speed of the car."""
        new_speed = self.statistics.current.speed + speed_mod
        min_speed = -(self.properties.max_speed / 2)
        max_speed = self.properties.max_speed

        return max(min_speed, min(new_speed, max_speed))

    def handle_controls(self, direction):
        """Handle the control input for the car."""
        current_speed = self.statistics.current.speed
        current_rotation = self.statistics.current.rotation
        properties = self.properties

        match (direction):
            case Direction.UP:
                current_speed = self.speed_limiter(properties.acceleration)
            case Direction.DOWN:
                current_speed = self.speed_limiter(-(properties.braking))
            case Direction.LEFT:
                if current_speed != 0:
                    self.rotation_direction = Direction.LEFT
                    current_rotation = (current_rotation - properties.handling) % 360
            case Direction.RIGHT:
                if current_speed != 0:
                    self.rotation_direction = Direction.RIGHT
                    current_rotation = (current_rotation + properties.handling) % 360

        self.statistics.current.speed = current_speed
        self.set_rotation(current_rotation)

    def move(self, timedelta, collisions):
        """Move the car, and handle collisions"""
        self.events.on_car_driving.notify(self)
        self.previous_position = self.position

        rad = math.radians(self.rotation)
        dx = self.current_speed * math.sin(rad) * timedelta
        dy = -self.current_speed * math.cos(rad) * timedelta

        if collisions:
            self.handle_collisions(collisions)
        else:
            if self.statistics.current.timeout > 0:
                self.statistics.current.timeout -= 1

        if self.timeout > self.tolerance:
            self.reset_to_last_checkpoint()
            return

        self.position[0] += dx
        self.position[1] += dy

    def handle_collisions(self, collisions):
        """Handle collisions with other objects."""
        for collision in collisions:
            if isinstance(collision, Car):
                self.statistics.current.speed *= 0.2
            else:
                self.statistics.current.timeout += 1
                self.statistics.current.speed *= 0.9

    def reset_to_last_checkpoint(self):
        """Reset the car to the last checkpoint."""
        self.penalties += 1
        self.statistics.current.timeout = 0
        self.statistics.current.speed = 0
        self.events.on_car_reset.notify(self)
