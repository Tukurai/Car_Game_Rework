import random
from types import SimpleNamespace
import pygame
from core.car import Car
from core.car_properties import CarProperties
from core.components.button_component import ButtonComponent
from core.components.countdown_component import CountdownComponent
from core.components.label_component import LabelComponent
from core.components.statistics_panel import StatisticsPanel
from core.enums.alignment import Alignment
from core.enums.log_level import LogLevel
from core.enums.scene import Scene
from core.enums.sprite_type import SpriteType
from core.position import Position
from core.relative import Relative
from core.services.sprite_service import SpriteService
from scenes.scene_base import SceneBase
from settings import Settings
from utilities.helper import Helper


class RaceScene(SceneBase):
    """The race scene, this is where the player will start racing."""

    def __init__(self, screen: pygame.surface, services: SimpleNamespace):
        super().__init__(screen, services)
        self.name = "race_scene"
        self.map = None
        self.players = []

        self.announcements = None
        self.started = False

        self.build_ui()

    def preload(self):
        if self.map is None:
            self.map = self.services.map.get_map("map_right")

            if len(self.players) < Settings.MAX_PLAYERS:
                self.services.logger.log(
                    f"not enough players, adding AI players",
                    LogLevel.DEBUG,
                )

                for i in range(Settings.MAX_PLAYERS - len(self.players)):
                    id_base = len(self.players)
                    self.add_player(self.create_ai_player(id_base + i))

            self.create_statistics_panels()

            for index, position, direction in self.map.get_start_positions(
                len(self.players)
            ):
                self.players[index].set_position(Position(position))
                self.players[index].set_rotation(direction.value * 90)

    def handle_event(self, event):
        super().handle_event(event)

        if (
            event.type == pygame.KEYUP
            and event.key == pygame.K_RETURN
            and not self.announcements.active
            and self.map is not None
        ):
            self.announcements.step()

        if self.map is not None:
            self.map.handle_event(event)

            for player in self.players:
                player.handle_event(event)

    def update(self, timedelta, input_state):
        super().update(timedelta, input_state)

        if self.started:
            for player in self.players:
                player.update(timedelta, input_state)

    def draw(self, screen, opacity: int = 255):
        if self.map is not None:
            self.map.draw(screen, opacity)

            for player in self.players:
                player.draw(screen, opacity)

        Helper.draw_outline(
            screen, (64, 64), (14 * 128, 7 * 128), (255, 255, 255), 2, opacity
        )

        super().draw(screen, opacity)

    def build_ui(self):
        """Build the UI for the scene."""

        race_label = LabelComponent(
            "scene_title",
            Position((self.screen.get_width() / 2, 32)),
            "Race!",
            Alignment.CENTER,
            50,
            parent=self,
        )
        self.components.append(race_label)

        announcement_label = CountdownComponent(
            "announcement_label",
            Position(
                (
                    self.screen.get_width() / 2,
                    Settings.MAP_OFFSET + (7 * Settings.TILE_SIZE) / 2,
                )
            ),
            [
                ("Press [ENTER] to begin countdown!", -1),
                ("3", 1),
                ("2", 1),
                ("1", 1),
                ("GO!", 0.25),
            ],
            Alignment.CENTER,
            50,
            parent=self,
        )
        self.components.append(announcement_label)
        self.announcements = announcement_label
        self.announcements.events.on_timeout_complete += self.start_race

    def create_statistics_panels(self):
        """Create the statistics panels for each player."""
        initial_position = Position(
            (Settings.MAP_OFFSET, self.screen.get_height() - 110)
        )
        for index, player in enumerate(self.players):
            statistics_panel = StatisticsPanel(
                f"car_statistics_id_{index}",
                player,
                Relative(initial_position, (index * 464, 0)),
                None,
                self,
            )
            self.components.append(statistics_panel)

    def add_player(self, player):
        """Add a player to the scene."""
        self.players.append(player)

    def create_ai_player(self, index: int):
        """Create an AI player."""
        ai_car_options = self.get_ai_car_options(index)
        return random.choice(ai_car_options)

    def get_ai_car_options(self, index: int):
        """Get the car options for the ai car"""
        return [
            Car(
                f"{color} AI Car {index}",
                self.services.sprite.get_sprite_from(SpriteType.VEHICLE, sprite),
                Position((0, 0)),
                properties,
            )
            for color, sprite, properties in Settings.CAR_OPTIONS
        ]

    def start_race(self, sender: CountdownComponent):
        self.started = True
