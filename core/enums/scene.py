from enum import Enum

class Scene(Enum):
    '''Enum for scenes, used by the SceneService, and scenes.'''
    MAINSCENE = 1
    RACESCENE = 2
    SCORESCENE = 3
    SINGLEPLAYERSCENE = 4
    MULTIPLAYER2PSCENE = 5
    MULTIPLAYER3PSCENE = 6
    MULTIPLAYER4PSCENE = 7
    SETTINGSSCENE = 8