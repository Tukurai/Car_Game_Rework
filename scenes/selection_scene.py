import copy
from types import SimpleNamespace
import pygame
from core.car_controls import CarControls
from core.car_properties import CarProperties
from core.components.button_component import ButtonComponent
from core.components.car_selection_panel import CarSelectionPanel
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.enums.direction import Direction
from core.enums.log_level import LogLevel
from core.enums.scene import Scene
from core.enums.sprite_type import SpriteType
from core.player_car import PlayerCar
from core.position import Position
from scenes.scene_base import SceneBase
from settings import Settings
from utilities.helper import Helper


class SelectionScene(SceneBase):
    """The selection scene, this is where the player will select their car, and track to start driving on."""

    def __init__(
        self, screen: pygame.surface, services: SimpleNamespace, player_count: int = 1
    ):
        super().__init__(screen, services)
        self.name = "selection_scene"
        self.player_count = player_count

        self.build_ui()

        # Notify that the scene is initialized
        self.events.on_scene_initialized.notify()

    def handle_event(self, event):
        super().handle_event(event)

    def update(self, timedelta, input_state):
        super().update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        super().draw(screen, opacity)

    def build_ui(self):
        """Build the UI for the scene."""

        race_label = LabelComponent(
            "scene_title",
            Position((self.screen.get_width() / 2, 150)),
            "Select your vehicle!",
            Alignment.CENTER,
            50,
            parent=self,
        )

        segment_positions = Helper.get_middle_positions(
            self.screen.get_width(), self.player_count
        )
        for i in range(self.player_count):
            player_car_selection = CarSelectionPanel(
                f"player_{i}_car_selection",
                i,
                self.get_car_options(),
                Position((segment_positions[i], 260)),
                self.services.sprite,
                parent=self,
            )
            player_car_selection.align(
                Alignment.CENTER, player_car_selection.scaled_size[0]
            )
            player_car_selection.events.on_player_ready += self.player_ready
            player_car_selection.events.on_log_message += self.services.logger.log
            self.components.append(player_car_selection)

        back_button = ButtonComponent(
            "back",
            Position((210, self.screen.get_height() - 70)),
            "Back",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        back_button.align(Alignment.RIGHT, back_button.scaled_size[0])
        back_button.events.on_button_clicked += self.back

        start_race_button = ButtonComponent(
            "start",
            Position((self.screen.get_width() - 210, self.screen.get_height() - 70)),
            "Start",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        start_race_button.align(Alignment.LEFT, start_race_button.scaled_size[0])
        start_race_button.events.on_button_clicked += self.start_race

        self.components.append(race_label)
        self.components.append(start_race_button)
        self.components.append(back_button)

    def start_race(self, sender: ButtonComponent):
        """Start the race scene."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)

        # check if all players are ready, and a track has been chosen.
        for component in self.components:
            if isinstance(component, CarSelectionPanel):
                if not component.ready:
                    self.services.logger.log(
                        f"player {component.player_id} is not ready", LogLevel.DEBUG
                    )
                    return

        self.services.scene.set_active_scene(Scene.RACESCENE)

    def player_ready(
        self, sender: CarSelectionPanel, player_id: int, nickname: str, car: PlayerCar
    ):
        """Handle the player ready event."""
        self.services.logger.log(
            f"player {player_id} ({nickname}) is ready, they chose the {car.name}.",
            LogLevel.DEBUG,
        )
        race = self.services.scene.get_scene(Scene.RACESCENE)
        car_copy = copy.copy(car)
        car_copy.name = nickname
        car_copy.controls = self.get_controls_for(player_id)
        race.add_player(car_copy)

    def get_controls_for(self, player_id: int):
        """Get the controls for the given player id."""
        controls = {
            0: CarControls( {
                Direction.UP: pygame.K_w,
                Direction.DOWN: pygame.K_s,
                Direction.LEFT: pygame.K_a,
                Direction.RIGHT: pygame.K_d,
            }),
            1: CarControls( {
                Direction.UP: pygame.K_UP,
                Direction.DOWN: pygame.K_DOWN,
                Direction.LEFT: pygame.K_LEFT,
                Direction.RIGHT: pygame.K_RIGHT,
            }),
            2: CarControls( {
                Direction.UP: pygame.K_t,
                Direction.DOWN: pygame.K_g,
                Direction.LEFT: pygame.K_f,
                Direction.RIGHT: pygame.K_h,
            }),
            3: CarControls( {
                Direction.UP: pygame.K_i,
                Direction.DOWN: pygame.K_k,
                Direction.LEFT: pygame.K_j,
                Direction.RIGHT: pygame.K_l,
            })
        }
        return controls[player_id]

    def back(self, sender: ButtonComponent):
        """return to the main menu."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.MAINSCENE)

    def get_car_options(self):
        """Get the car options for the car selection panel"""
        return [
            PlayerCar(
                f"{color} Car",
                self.services.sprite.get_sprite_from(SpriteType.VEHICLE, sprite),
                None,
                Position((0, 0)),
                properties,
            )
            for color, sprite, properties in Settings.CAR_OPTIONS
        ]