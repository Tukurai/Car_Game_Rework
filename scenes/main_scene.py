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
from scenes.scene_base import SceneBase


class MainScene(SceneBase):
    """The main scene, the first scene to be shown when the game starts."""

    def __init__(self, screen: pygame.surface, services: SimpleNamespace):
        super().__init__(screen, services)
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
            Position((self.screen.get_width() / 2, 150)),
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
        singleplayer_button.events.on_button_clicked += self.singleplayer_start

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
        multiplayer_button.events.on_button_clicked += self.multiplayer_start

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
        highscores_button.events.on_button_clicked += self.show_highscores

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
        settings_button.events.on_button_clicked += self.show_settings

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
        exit_button.events.on_button_clicked += self.exit_game

        self.components.append(race_label)
        self.components.append(singleplayer_button)
        self.components.append(multiplayer_button)
        self.components.append(highscores_button)
        self.components.append(settings_button)
        self.components.append(exit_button)

    def singleplayer_start(self, sender: ButtonComponent):
        """Start the singleplayer scene."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.SINGLEPLAYERSCENE)

    def multiplayer_start(self, sender: ButtonComponent):
        """Start the multiplayer scene."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.MULTIPLAYERSCENE)

    def show_highscores(self, sender: ButtonComponent):
        """Start the highscores scene."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.SCORESCENE)

    def show_settings(self, sender: ButtonComponent):
        """Start the settings scene."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        self.services.scene.set_active_scene(Scene.SETTINGSSCENE)

    def exit_game(self, sender: ButtonComponent):
        """Exit the game."""
        self.services.logger.log(f"clicked on {sender.name}", LogLevel.DEBUG)
        pygame.event.post(pygame.event.Event(pygame.QUIT))