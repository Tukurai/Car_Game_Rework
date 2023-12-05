class ServiceBase():
    """Base class for all services. Gives some standard functionality."""
    def __init__(self):
        pass

    def handle_event(self, event):
        """Handle any non pygame.QUIT event."""
        pass

    def update(self, timedelta, imput_state):
        """Update the game state for all relevant sources."""
        pass

    def draw(self):
        """Draw the game state."""
        pass