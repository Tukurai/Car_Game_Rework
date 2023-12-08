from enum import Enum

class SpriteType(Enum):
    '''Enum for sprite types, used by the Sprite service class.'''
    GLOBAL = 0
    VEHICLE = 1
    OBJECT = 2
    TILE = 3
    UI = 4