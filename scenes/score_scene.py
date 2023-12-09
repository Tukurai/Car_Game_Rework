from types import SimpleNamespace
import pygame
from core.components.button_component import ButtonComponent
from core.enums.alignment import Alignment
from core.enums.log_level import LogLevel
from core.enums.scene import Scene
from core.enums.sprite_type import SpriteType
from core.position import Position
from core.services.sprite_service import SpriteService
from scenes.scene_base import SceneBase


class ScoreScene(SceneBase):
    """The score scene, this is where the player will see their score, and other highscores."""

    def __init__(self, screen: pygame.surface, services: SimpleNamespace):
        super().__init__(screen, services)
        self.name = "score_scene"

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

        self.components.append(back_button)

    def back(self, sender: ButtonComponent):
        """return to the main menu."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.MAINSCENE)