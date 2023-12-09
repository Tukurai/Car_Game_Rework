from types import SimpleNamespace
import pygame
from core.components.button_component import ButtonComponent
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.enums.log_level import LogLevel
from core.enums.scene import Scene
from core.enums.sprite_type import SpriteType
from core.position import Position
from core.relative import Relative
from core.services.sprite_service import SpriteService
from scenes.scene_base import SceneBase


class SelectionScene(SceneBase):
    """The selection scene, this is where the player will select their car, and track to start driving on."""

    def __init__(self, screen: pygame.surface, services: SimpleNamespace, player_count: int = 1):
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

    def draw(self, screen):
        super().draw(screen)


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

        back_button = ButtonComponent(
            "back",
            Position((210, self.screen.get_height() - 70 )),
            "Back",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        back_button.align(Alignment.RIGHT)
        back_button.events.on_button_clicked += self.back
        
        start_race_button = ButtonComponent(
            "start",
            Position((self.screen.get_width() - 210, self.screen.get_height() - 70 )),
            "Start",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        start_race_button.align(Alignment.LEFT)
        start_race_button.events.on_button_clicked += self.start_race

        self.components.append(race_label)
        self.components.append(start_race_button)
        self.components.append(back_button)

    def start_race(self, sender: ButtonComponent):
        """Start the race scene."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)

        # check if all players are ready, and a track has been chosen.
        self.services.scene.set_active_scene(Scene.RACESCENE)

    def back(self, sender: ButtonComponent):
        """return to the main menu."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.MAINSCENE)
