import math
from injector import inject
from types import SimpleNamespace

import pygame
from core.components.label_component import LabelComponent
from core.enums.alignment import Alignment
from core.enums.log_level import LogLevel
from core.enums.scene import Scene
from core.event_handler import EventHandler
from core.position import Position
from core.services.log_service import LogService
from core.services.map_service import MapService
from core.services.service_base import ServiceBase
from core.services.sound_service import SoundService
from core.services.sprite_service import SpriteService
from scenes.main_scene import MainScene
from scenes.race_scene import RaceScene
from scenes.score_scene import ScoreScene
from scenes.selection_scene import SelectionScene
from scenes.settings_scene import SettingsScene
from settings import Settings


class SceneService(ServiceBase):
    @inject
    def __init__(
        self,
        log_service: LogService,
        sprite_service: SpriteService,
        sound_service: SoundService,
        map_service: MapService,
        settings: Settings,
        screen: pygame.Surface,
    ):
        super().__init__(settings)
        self.services.logger = log_service
        self.services.sprite = sprite_service
        self.services.sound = sound_service
        self.services.map = map_service
        self.services.scene = self
        self.scenes = []
        self.active_scene = None
        self.screen = screen
        self.fps_label = LabelComponent(
            "fps_label",
            Position((30, 10)),
            "",
            Alignment.CENTER,
            16,
            parent=self,
        )

        self.transition = SimpleNamespace(
            active=False,
            next_scene=None,
            next_scene_opacity=0,
        )

        # Create events
        self.events.on_scene_changing = EventHandler()
        self.events.on_scene_changed = EventHandler()

        # Add event handlers
        self.events.on_scene_changing += self.handle_scene_changing
        self.events.on_scene_changed += self.handle_scene_changed

    def initialize_scenes(self):
        """Create all the scenes store them in a dictionary, using the Scene Enum as a key."""
        self.scenes = {
            Scene.MAINSCENE: MainScene(self.screen, self.services),
            Scene.SINGLEPLAYERSCENE: SelectionScene(self.screen, self.services, 1),
            Scene.MULTIPLAYER2PSCENE: SelectionScene(self.screen, self.services, 2),
            Scene.MULTIPLAYER3PSCENE: SelectionScene(self.screen, self.services, 3),
            Scene.MULTIPLAYER4PSCENE: SelectionScene(self.screen, self.services, 4),
            Scene.RACESCENE: RaceScene(self.screen, self.services),
            Scene.SCORESCENE: ScoreScene(self.screen, self.services),
            Scene.SETTINGSSCENE: SettingsScene(self.screen, self.services),
        }

    def get_scene(self, scene: Scene):
        """Get a scene by its enum."""
        return self.scenes[scene]

    def set_active_scene(self, next_scene: Scene):
        """Set the active scene."""
        if not self.transition.active and self.active_scene != None:
            self.events.on_scene_changing.notify(next_scene)
            self.get_scene(next_scene).preload()
            self.transition.active = True
            self.transition.next_scene = next_scene
            self.transition.next_scene_opacity = 0
        else:
            self.events.on_scene_changed.notify(next_scene)
            self.active_scene = self.scenes[next_scene]
            self.transition.active = False
            self.transition.next_scene_opacity = 0
            self.transition.next_scene = None

    def handle_event(self, event):
        """Handle any non pygame.QUIT event. The event is passed down to the active scene."""
        if self.transition.active:
            self.get_scene(self.transition.next_scene).handle_event(event)
        elif self.active_scene:
            self.active_scene.handle_event(event)

    def update(self, timedelta, input_state):
        """Update the game state for all relevant sources."""
        self.fps_label.text = f"FPS: {1 // timedelta}"

        if self.transition.active:
            transition_tick = 255 / (
                math.floor(Settings.TRANSITION_SPEED * Settings.FPS)
            )
            self.transition.next_scene_opacity += transition_tick
            self.get_scene(self.transition.next_scene).update(timedelta, input_state)
            if self.transition.next_scene_opacity >= 255:
                self.set_active_scene(self.transition.next_scene)
        elif self.active_scene:
            self.active_scene.update(timedelta, input_state)

    def draw(self, screen):
        """Draw the active screen's components."""
        if self.transition.active:
            self.get_scene(self.transition.next_scene).draw(
                self.screen, self.transition.next_scene_opacity
            )
        elif self.active_scene:
            self.active_scene.draw(self.screen, 255)

        self.fps_label.draw(self.screen)

    # ------------------------------
    # Event handlers
    # ------------------------------
    def handle_scene_changed(self, next_scene):
        """Handle the scene change event."""
        active_scene_name = self.active_scene.name if self.active_scene else "None"
        self.services.logger.log(
            f"Scene changed {active_scene_name} to {self.scenes[next_scene].name}",
            LogLevel.INFO,
        )

    def handle_scene_changing(self, next_scene):
        """Handle the scene changing event."""
        active_scene_name = self.active_scene.name if self.active_scene else "None"
        self.services.logger.log(
            f"Scene changing {active_scene_name} to {self.scenes[next_scene].name}",
            LogLevel.INFO,
        )
