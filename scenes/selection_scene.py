import pygame
from core.services.sprite_service import SpriteService
from scenes.scene_base import SceneBase


class SelectionScene(SceneBase):
    """The selection scene, this is where the player will select their car, and track to start driving on."""

    def __init__(self, screen: pygame.surface, sprite_service: SpriteService):
        super().__init__(screen, sprite_service)
        self.name = "selection_scene"

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
        pass
