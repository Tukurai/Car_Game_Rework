from core.car import Car
from core.car_controls import CarControls
from core.car_properties import CarProperties
from core.enums.direction import Direction
from core.input_state import InputState
from core.position import Position
from core.sprites.sprite import Sprite


class PlayerCar(Car):
    """Class for handeling a PlayerCar."""

    def __init__(
        self,
        name: str,
        image: Sprite,
        controls: CarControls,
        position: Position,
        properties: CarProperties,
    ):
        super().__init__(name, image, position, properties)
        self.controls = controls

    def update(self, delta_time: float, input_state: InputState):
        keys = input_state.cur_keyboard_state

        if keys[self.controls.get_key(Direction.UP)]:
            self.handle_controls(Direction.UP)
        elif keys[self.controls.get_key(Direction.DOWN)]:
            self.handle_controls(Direction.DOWN)
        else:
            self.apply_drag()

        if keys[self.controls.get_key(Direction.LEFT)]:
            self.handle_controls(Direction.LEFT)
        elif keys[self.controls.get_key(Direction.RIGHT)]:
            self.handle_controls(Direction.RIGHT)

        super().update(delta_time, input_state)
