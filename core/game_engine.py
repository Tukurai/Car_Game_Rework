from injector import inject
import pygame
import pymunk
from core.input_state import InputState
from core.services.scene_service import SceneService
from core.services.score_service import ScoreService

from settings import Settings


class GameEngine:
    """A class to represent the game engine, responsible for the game loop and thus updating the services."""

    @inject
    def __init__(
        self,
        screen: pygame.Surface,
        space: pymunk.Space,
        input_state: InputState,
        settings: Settings,
        sceneservice: SceneService,
        scoreservice: ScoreService,
    ):
        self.input_state = input_state
        self.screen = screen
        self.space = space
        self.settings = settings
        self.sceneservice = sceneservice
        self.scoreservice = scoreservice
        self.clock = pygame.time.Clock()

    def run_game_loop(self):
        """Run the game loop as long as running is true, sending the pygame.event QUIT will gracefully end the loop."""
        running = True
        while running:
            timedelta = self.clock.tick(self.settings.fps) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    self.handle_event(event)

            # Update input state
            self.input_state.update()

            # Update physics
            self.update(timedelta)

            # Drawing
            self.draw()

            # Flip the display
            pygame.display.flip()

    def handle_event(self, event):
        """Handle any non pygame.QUIT event. The event is passed down to all relevant services."""
        self.sceneservice.handle_event(event)
        self.scoreservice.handle_event(event)

    def update(self, timedelta):
        """Update the game state for all relevant sources."""

        self.sceneservice.update(timedelta, self.input_state)

    def draw(self):
        """Draw the game state."""
        # Draw background
        self.screen.fill((0, 0, 0))

        # Draw all relevant services
        self.sceneservice.draw()
