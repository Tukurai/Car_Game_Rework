from types import SimpleNamespace
from core.components.button_component import ButtonComponent
from core.components.car_options_panel import CarOptionsPanel
from core.components.component_base import ComponentBase
from core.components.textbox_component import TextboxComponent
from core.event_handler import EventHandler
from core.position import Position
from core.relative import Relative


class CarSelectionPanel(ComponentBase):
    """Panel for selecting a car, and displaying information about the selected car"""

    def __init__(self, name, position: Position = Position((0, 0)), parent=None):
        super().__init__(name, position, parent)
        self.ready = False

        self.player_name_textbox = TextboxComponent(
            "player_name", Position((0, 0)), self
        )
        self.add_child(self.player_name_textbox)

        self.car_options = CarOptionsPanel(
            "car_options", Relative(self.position, (0, 0)), self
        )
        self.add_child(self.car_options)

        self.ready_check = ButtonComponent(
            "ready_check", Relative(self.position, (0, 0)), self
        )
        self.add_child(self.ready_check)

        # Create events namespace
        self.events = SimpleNamespace()
        self.events.on_car_selected = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event"""
        return

    def update(self, timedelta, input_state):
        """Update the component and all its children"""
        if not self.ready:  # If the component is ready to proceed, don't update the children
            super().update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children"""
        super().draw(screen, opacity)
