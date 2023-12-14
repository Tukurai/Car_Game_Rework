from types import SimpleNamespace
from core.enums.alignment import Alignment

from core.event_handler import EventHandler
from core.position import Position


class ComponentBase:
    """Base class for all components, every component should inherit from this class"""

    def __init__(self, name, position: Position = Position((0, 0)), alignment: Alignment=None, parent=None):
        self.name = name
        self.parent = parent
        self.children = []
        self.position = position
        self.alignment = alignment

        # Create events namespace
        self.events = SimpleNamespace()
        self.events.on_log_message = EventHandler()

    def initialize(self):
        """Initialize the component"""
        pass

    def handle_event(self, event):
        """Handle any non pygame.QUIT event"""
        for child in self.children:
            child.handle_event(event)

    def update(self, timedelta, input_state):
        """Update the component and all its children"""
        for child in self.children:
            child.update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        """Draw the component and all its children"""
        for child in self.children:
            child.draw(screen, opacity)

    def align(self, alignment: Alignment, width):
        """Align the button to the center of the position."""
        self.restore_alignment(self.alignment, width)

        if self.alignment != alignment:
            match alignment:
                case Alignment.CENTER:
                    self.position.x -= width / 2
                case Alignment.RIGHT:
                    self.position.x -= width

    def restore_alignment(self, alignment: Alignment, width):
        """Restore the alignment of the component."""
        if alignment is None:
            return
        
        match alignment:
            case Alignment.CENTER:
                self.position.x += width / 2
            case Alignment.RIGHT:
                self.position.x += width
