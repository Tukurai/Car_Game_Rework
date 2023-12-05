import pygame
import pymunk
from injector import Injector, singleton
from core.game_engine import GameEngine
from core.input_state import InputState
from core.services.collision_service import CollisionService
from core.services.map_service import MapService
from core.services.scene_service import SceneService
from core.services.score_service import ScoreService
from core.services.sound_service import SoundService
from core.services.sprite_service import SpriteService

from settings import Settings


class DI():
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if DI.__instance == None:
            DI()
        return DI.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if DI.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            DI.__instance = self
            self.injector = Injector(self.configure_dependencies)

    def configure_dependencies(self, binder):
        pygame.init()

        settings = Settings()

        screen = pygame.display.set_mode(settings.resolution)
        space = pymunk.Space()

        binder.bind(pygame.Surface, to=screen, scope=singleton)
        binder.bind(pymunk.Space, to=space, scope=singleton)
        binder.bind(Settings, to=settings, scope=singleton)
        binder.bind(InputState, to=InputState(), scope=singleton)

        binder.bind(CollisionService, to=CollisionService(), scope=singleton)
        binder.bind(MapService, to=MapService(), scope=singleton)
        binder.bind(SceneService, to=SceneService(), scope=singleton)
        binder.bind(ScoreService, to=ScoreService(), scope=singleton)
        binder.bind(SoundService, to=SoundService(), scope=singleton)
        binder.bind(SpriteService, to=SpriteService(), scope=singleton)

    def get(self, obj):
        return self.injector.get(obj)
