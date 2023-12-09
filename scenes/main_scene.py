import pygame
from core.components.button_component import ButtonComponent
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.enums.sprite_type import SpriteType
from core.position import Position
from core.relative import Relative
from core.services.sprite_service import SpriteService
from scenes.scene_base import SceneBase


class MainScene(SceneBase):
    """The main scene, the first scene to be shown when the game starts."""

    def __init__(self, screen: pygame.surface, sprite_service: SpriteService):
        super().__init__(screen, sprite_service)
        self.name = "main_scene"

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

        button_y_offset = 60

        race_label = LabelComponent(
            "race_title",
            Position((self.screen.get_width() / 2, 200)),
            "Fantastic Race Game",
            Alignment.CENTER,
            50,
            parent=self,
        )

        singleplayer_button = ButtonComponent(
            "singleplayer",
            Relative(race_label.position, (0, button_y_offset)),
            "Singleplayer",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        singleplayer_button.align(Alignment.CENTER)

        multiplayer_button = ButtonComponent(
            "multiplayer",
            Relative(singleplayer_button.position, (0, button_y_offset)),
            "Multiplayer",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        highscores_button = ButtonComponent(
            "highscores",
            Relative(multiplayer_button.position, (0, button_y_offset)),
            "Highscores",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        settings_button = ButtonComponent(
            "settings",
            Relative(highscores_button.position, (0, button_y_offset)),
            "Settings",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )
        exit_button = ButtonComponent(
            "exit",
            Relative(settings_button.position, (0, button_y_offset)),
            "Exit",
            30,
            self.services.sprite.get_sprite_from(SpriteType.UI, "blue_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button00.png"),
            self.services.sprite.get_sprite_from(SpriteType.UI, "green_button01.png"),
            parent=self,
        )

        self.components.append(race_label)
        self.components.append(singleplayer_button)
        self.components.append(multiplayer_button)
        self.components.append(highscores_button)
        self.components.append(settings_button)
        self.components.append(exit_button)
