from types import SimpleNamespace
from injector import inject
import pygame
from core.event_handler import EventHandler
from core.services.sprite_service import SpriteService


class SceneBase:
    """The base class for all scenes."""

    def __init__(self, screen: pygame.surface, sprite_service: SpriteService):
        """Initialize the scene with a name and a list of components. Also fetch the services from the DI container."""
        self.name = "base_scene"
        self.scene = None
        self.screen = screen
        self.components = []

        # services
        self.services = SimpleNamespace()
        self.services.sprite = sprite_service

        self.initialize_components()

        # Create events
        self.events = SimpleNamespace()
        self.events.on_scene_initialized = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event."""
        for component in self.components:
            component.handle_event(event)
        pass

    def update(self, timedelta, input_state):
        """Update the scene and all its components."""
        for component in self.components:
            component.update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        """Draw the scene and all its components."""
        for component in self.components:
            component.draw(screen, opacity)

    def initialize_components(self):
        """Create all components and initialize them."""
        for component in self.components:
            component.initialize()
