from types import SimpleNamespace
from injector import inject
import pygame
from core.enums.scene import Scene
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
        settings: Settings,
        scene_service: SceneService,
        score_service: ScoreService,
    ):
        self.input_state = InputState()
        self.screen = screen
        self.settings = settings
        self.clock = pygame.time.Clock()

        self.services = SimpleNamespace()
        self.services.scene = scene_service
        self.services.score = score_service


    def run_game_loop(self):
        """Run the game loop as long as running is true, sending the pygame.event QUIT will gracefully end the loop."""
        self.services.scene.initialize_scenes()
        self.services.scene.set_active_scene(Scene.MAINSCENE)

        running = True
        while running:
            timedelta = self.clock.tick(Settings.FPS) / 1000.0

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
        self.services.scene.handle_event(event)

    def update(self, timedelta):
        """Update the game state for all relevant sources."""

        self.services.scene.update(timedelta, self.input_state)

    def draw(self):
        """Draw the game state."""
        # Draw background
        self.screen.fill((0, 0, 0))

        # Draw all relevant services
        self.services.scene.draw(self.screen)
