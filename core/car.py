import copy
import math
from types import SimpleNamespace

import pygame
from core.car_properties import CarProperties
from core.car_statistics import CarStatistics
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
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

        self.sprite.position = self.position

        self.name_label = LabelComponent(
            f"{self.name}_name",
            Relative(self.position, (0, -20)),
            self.name,
            Alignment.CENTER,
            14,
            color=(255, 255, 255),
            outline_color=(0, 0, 0),
            parent=self,
        )

        # Create events
        self.events = SimpleNamespace()
        self.events.on_car_driving = EventHandler()
        self.events.on_car_reset = EventHandler()

    def set_position(self, position: Position):
        """Set the position of the car, also altering the sprite position relatively.
        Replacing the position property will not alter the sprite position."""
        self.position = position
        self.sprite.position = self.position
        self.name_label.position = Relative(self.position, (0, -20))

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
        self.statistics.update()

    def draw(self, screen, opacity: int = 255):
        """Draw the car."""
        # Draw the car
        self.sprite.draw(screen, opacity)

        # Draw the name
        self.name_label.draw(screen, opacity)

    def handle_event(self, event):
        """Handle any non pygame.QUIT event."""
        return

    def apply_drag(self):
        """Apply drag to the car, decreasing the speed."""
        speed = self.statistics.current.speed
        if speed == 0:
            return

        drag = self.properties.drag

        if drag > abs(speed):
            self.statistics.current.speed = 0
        else:
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
                current_speed = self.speed_limiter(
                    -(
                        properties.braking
                        if self.statistics.current.speed > 0
                        else properties.acceleration
                    )
                )
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
        self.previous_position = copy.copy(self.position)

        rad = math.radians(self.statistics.current.rotation)
        direction_x = self.statistics.current.speed * math.sin(rad) * timedelta
        direction_y = -self.statistics.current.speed * math.cos(rad) * timedelta

        if collisions:
            self.handle_collisions(collisions)
        else:
            if self.statistics.current.tolerance > 0:
                self.statistics.current.tolerance -= 1

        if self.statistics.current.tolerance > self.properties.tolerance:
            self.reset_to_last_checkpoint()
            return

        new_position = Position(self.position + Position((direction_x, direction_y)))
        self.set_position(new_position)

    def handle_collisions(self, collisions):
        """Handle collisions with other objects."""
        for collision in collisions:
            if isinstance(collision, Car):
                self.statistics.current.speed *= 0.2
            else:
                self.statistics.current.tolerance += 1
                self.statistics.current.speed *= 0.9

    def reset_to_last_checkpoint(self):
        """Reset the car to the last checkpoint."""
        self.penalties += 1
        self.statistics.current.tolerance = 0
        self.statistics.current.speed = 0
        self.events.on_car_reset.notify(self)
