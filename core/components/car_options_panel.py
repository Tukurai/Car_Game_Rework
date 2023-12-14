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


class CarOptionsPanel(ComponentBase):
    """Panel for choosing a car, displaying information about the car."""

    def __init__(
        self,
        name,
        cars: list[Car],
        position: Position = Position((0, 0)),
        alignment: Alignment = None,
        parent=None,
    ):
        super().__init__(name, position, alignment, parent)
        self.ready = False
        self.cars = cars
        self.selected_car = None
        self.selected_button = None
        self.scaled_size = (400, 600)

        segment_positions = Helper.get_middle_positions(
            self.parent.scaled_size[0], len(cars)
        )
        for i in range(len(cars)):
            car_option = ButtonComponent(
                cars[i].name,
                Relative(self.position, (segment_positions[i], 0)),
                "",
                30,
                cars[i].sprite,
                cars[i].sprite,
                cars[i].sprite,
                parent=self,
            )
            car_option.align(Alignment.CENTER, car_option.scaled_size[0])
            car_option.events.on_button_clicked += self.car_selected
            self.children.append(car_option)

        self.create_labels()
        self.create_values()

        # Create events namespace
        self.events = SimpleNamespace()
        self.events.on_car_selected = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event"""
        super().handle_event(event)

    def update(self, timedelta, input_state):
        """Update the component and all its children, if the component is ready to proceed, don't update the children"""
        if not self.ready:
            super().update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children"""
        if self.selected_button is not None:
            Helper.draw_outline(
                screen,
                self.selected_button.position.get_pos(),
                self.selected_button.scaled_size,
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

    def create_labels(self):
        """Create the labels for the car information."""
        label_spacing = 40
        labels = [
            ("car_name_label", "Car name:"),
            ("car_max_speed_label", "Max speed:"),
            ("car_acceleration_label", "Acceleration:"),
            ("car_braking_label", "Braking:"),
            ("car_handling_label", "Handling:"),
            ("car_drag_label", "Drag:"),
            ("car_tolerance_label", "Tolerance:"),
        ]

        for i, (label_name, label_text) in enumerate(labels):
            label = LabelComponent(
                label_name,
                Relative(self.position, (30, 80 + i * label_spacing)),
                label_text,
                Alignment.LEFT,
                30,
                parent=self,
            )
            self.children.append(label)

    def create_values(self):
        """Create the labels for the car information values."""
        label_spacing = 40
        labels = [
            ("car_name_label_value", "Pick a car"),
            ("car_max_speed_label_value", "0 pp/u"),
            ("car_acceleration_label_value", "0 pp/u"),
            ("car_braking_label_value", "0 pp/u"),
            ("car_handling_label_value", "0 dg/u"),
            ("car_drag_label_value", "0 pp/u"),
            ("car_tolerance_label_value", "0 ob/s"),
        ]

        for i, (label_name, label_text) in enumerate(labels):
            label = LabelComponent(
                label_name,
                Relative(
                    self.position, (self.scaled_size[0] - 30, 80 + i * label_spacing)
                ),
                label_text,
                Alignment.RIGHT,
                30,
                parent=self,
            )
            self.children.append(label)

    def show_car_info(self):
        """Show the car information."""
        car = self.selected_car
        labels = [
            ("car_name_label_value", car.name),
            ("car_max_speed_label_value", f"{car.properties.max_speed} pp/u"),
            ("car_acceleration_label_value", f"{car.properties.acceleration} pp/u"),
            ("car_braking_label_value", f"{car.properties.braking} pp/u"),
            ("car_handling_label_value", f"{car.properties.handling} dg/u"),
            ("car_drag_label_value", f"{car.properties.drag} pp/u"),
            ("car_tolerance_label_value", f"{car.properties.tolerance} ob/s"),
        ]

        for child in self.children:
            if child.name in [label[0] for label in labels]:
                child.text = [label[1] for label in labels if label[0] == child.name][0]

    def car_selected(self, sender: ButtonComponent):
        """Notify that a car has been selected."""
        self.selected_car = self.get_car_by_name(sender.name)
        self.selected_button = sender
        self.show_car_info()
        self.events.on_car_selected.notify(sender, self.selected_car)
