from enum import Enum

class TileType(Enum):
    '''Enum for tile types, used by the Map class.'''
    GROUND = 0
    ROAD = 1
    OBJECT = 2
    CHECKPOINT = 3