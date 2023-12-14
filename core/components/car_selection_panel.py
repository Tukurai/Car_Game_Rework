from types import SimpleNamespace
from core.car_properties import CarProperties
from core.components.button_component import ButtonComponent
from core.components.car_options_panel import CarOptionsPanel
from core.components.component_base import ComponentBase
from core.components.label_component import LabelComponent
from core.components.textbox_component import TextboxComponent
from core.enums.alignment import Alignment
from core.enums.log_level import LogLevel
from core.enums.sprite_type import SpriteType
from core.event_handler import EventHandler
from core.player_car import PlayerCar
from core.position import Position
from core.relative import Relative
from core.services.sprite_service import SpriteService
from utilities.helper import Helper


class CarSelectionPanel(ComponentBase):
    """Panel for selecting a car, and displaying information about the selected car"""

    def __init__(
        self,
        name: str,
        player_id: int,
        cars: list[PlayerCar],
        position: Position,
        sprite_service: SpriteService,
        alignment: Alignment = None,
        parent=None,
    ):
        super().__init__(name, position, alignment, parent)
        self.player_id = player_id
        self.scaled_size = (400, 600)
        self.ready = False

        self.services = SimpleNamespace()
        self.services.sprite = sprite_service

        self.player_name_textbox = TextboxComponent(
            f"player_name_{self.player_id}",
            Relative(self.position, (self.scaled_size[0] - 30, 40)),
            "",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button13.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button13.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button13.png"),
            parent=self,
        )
        self.player_name_textbox.align(
            Alignment.RIGHT, self.player_name_textbox.scaled_size[0]
        )
        self.children.append(self.player_name_textbox)

        self.player_name_label = LabelComponent(
            f"player_name_label_{self.player_id}",
            Relative(self.position, (30, 60)),
            "Nickname:",
            Alignment.LEFT,
            36,
            parent=self,
        )
        self.children.append(self.player_name_label)

        self.car_options = CarOptionsPanel(
            f"car_options_{self.player_id}",
            cars,
            Relative(self.position, (self.scaled_size[0] / 2, 120)),
            parent=self,
        )
        self.car_options.align(Alignment.CENTER, self.scaled_size[0])
        self.children.append(self.car_options)

        self.ready_check = ButtonComponent(
            f"ready_check_{self.player_id}",
            Relative(
                self.position, (self.scaled_size[0] / 2, self.scaled_size[1] - 70)
            ),
            "Ready",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        self.ready_check.align(Alignment.CENTER, self.ready_check.scaled_size[0])
        self.ready_check.events.on_button_clicked += self.ready_clicked
        self.children.append(self.ready_check)

        # Create events namespace
        self.events = SimpleNamespace()
        self.events.on_player_ready = EventHandler()
        self.events.on_log_message = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event, if the component is ready to proceed, don't handle the event"""
        if not self.ready:
            super().handle_event(event)

    def update(self, timedelta, input_state):
        """Update the component and all its children, if the component is ready to proceed, don't update the children"""
        if not self.ready:
            super().update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children"""
        if self.ready:
            Helper.draw_outline(
                screen,
                self.position.get_pos(),
                self.scaled_size,
                (255, 255, 255),
                2,
                opacity,
            )
            
        super().draw(screen, opacity)

    def ready_clicked(self, sender: ButtonComponent):
        """Notify that the player is ready to proceed."""
        nickname = self.player_name_textbox.get_value()
        car = self.car_options.selected_car
        if nickname == "":
            self.events.on_log_message.notify(
                f"Player {self.player_id} has no nickname", LogLevel.INFO
            )
            return
        if car is None:
            self.events.on_log_message.notify(
                f"Player {self.player_id} has no selected car", LogLevel.INFO
            )
            return

        self.ready = True
        self.events.on_player_ready.notify(self, self.player_id, nickname, car)
