from types import SimpleNamespace

from core.event_handler import EventHandler
from core.position import Position


class ComponentBase:
    """Base class for all components, every component should inherit from this class"""

    def __init__(self, name, position: Position = Position((0, 0)), parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.position = position

        # Create events namespace
        self.events = SimpleNamespace()
        self.events.on_log_message = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event"""
        return

    def update(self, timedelta, input_state):
        """Update the component and all its children"""
        for child in self.children:
            child.update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children"""
        for child in self.children:
            child.draw(screen, opacity)
