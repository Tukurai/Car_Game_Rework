from injector import inject
from types import SimpleNamespace
from core.event_handler import EventHandler
from settings import Settings


class ServiceBase:
    """Base class for all services. Gives some standard functionality."""

    @inject
    def __init__(self, settings:Settings):
        """Initialize the service with a name and a list of components. Also fetch the services from the DI container. Child classes are responsible for notifying the initialization finishing."""
        self.settings = settings

        self.services = SimpleNamespace()

        # Create events
        self.events = SimpleNamespace()
        self.events.on_service_initialized = EventHandler()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event."""
        pass

    def update(self, timedelta, imput_state):
        """Update the game state for all relevant sources."""
        pass

    def draw(self):
        """Draw the game state."""
        pass
