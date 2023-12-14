from types import SimpleNamespace

import pygame
from core.car import Car
from core.components.button_component import ButtonComponent
from core.components.component_base import ComponentBase
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.event_handler import EventHandler
from core.position import Position
from core.relative import Relative
from utilities.helper import Helper


class StatisticsPanel(ComponentBase):
    """A panel that shows the statistics of the car related to it."""

    def __init__(
        self,
        name,
        car: Car,
        position: Position = Position((0, 0)),
        alignment: Alignment = None,
        parent=None,
    ):
        super().__init__(name, position, alignment, parent)
        self.car = car
        self.scaled_size = (400, 100)

        self.create_labels()
        self.create_values()

    def handle_event(self, event):
        """This component does not handle events."""
        return

    def update(self, timedelta, input_state):
        """Update the component and all its children, if the component is ready to proceed, don't update the children"""
        super().update(timedelta, input_state)

        self.show_car_info()

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children"""
        Helper.draw_outline(
            screen,
            self.position.get_pos(),
            self.scaled_size,
            (255, 255, 255),
            2,
            opacity,
        )

        super().draw(screen, opacity)

    def get_car_by_name(self, car_name) -> Car:
        for car in self.cars:
            if car.name == car_name:
                return car
        return None

    def create_label_components(self, labels, x_position, alignment):
        """Helper method to create and append LabelComponent objects."""
        label_spacing = 22
        for i, (label_name, label_text) in enumerate(labels):
            label = LabelComponent(
                label_name,
                Relative(self.position, (x_position, 16 + i * label_spacing)),
                label_text,
                alignment,
                24,
                parent=self,
            )
            self.children.append(label)

    def create_labels(self):
        """Create the labels for the car information."""
        car_labels = [
            ("car_name_label", "Car name:"),
            ("car_speed_label", "Speed:"),
            ("car_rotation_label", "Rotation:"),
            ("car_tolerance_label", "Tolerance:"),
        ]
        self.create_label_components(car_labels, 12, Alignment.LEFT)

        player_labels = [
            ("car_lap_label", f"Lap:"),
            ("car_penalty_label", f"Penalties:"),
            ("car_score_label", f"Score:"),
            ("car_place_label", f"Placing:"),
        ]
        self.create_label_components(player_labels, 240, Alignment.LEFT)

    def create_values(self):
        """Create the labels for the car information values."""
        car_labels = [
            ("car_name_label_value", "Please wait..."),
            ("car_speed_label_value", "0 pp/u"),
            ("car_rotation_label_value", "0 deg."),
            ("car_tolerance_label_value", "0 col."),
        ]
        self.create_label_components(car_labels, 210, Alignment.RIGHT)

        player_labels = [
            ("car_lap_label_value", f"-"),
            ("car_penalty_label_value", f"-"),
            ("car_score_label_value", f"-"),
            ("car_place_label_value", f"-"),
        ]
        self.create_label_components(player_labels, 388, Alignment.RIGHT)

    def show_car_info(self):
        """Show the car information."""
        car = self.car
        labels = [
            ("car_name_label_value", car.name),
            ("car_speed_label_value", f"{car.statistics.current.speed} pp/u"),
            ("car_rotation_label_value", f"{car.statistics.current.rotation} deg."),
            ("car_tolerance_label_value", f"{car.statistics.current.tolerance} col."),
            ("car_lap_label_value", f"{car.lap}"),
            ("car_penalty_label_value", f"{car.penalties}"),
            ("car_score_label_value", f"{car.score}"),
            ("car_place_label_value", f"{car.place}"),
        ]

        for child in self.children:
            if child.name in [label[0] for label in labels]:
                child.text = [label[1] for label in labels if label[0] == child.name][0]

        
