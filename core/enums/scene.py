from enum import Enum

class Scene(Enum):
    '''Enum for scenes, used by the SceneService, and scenes.'''
    MAINSCENE = 1
    RACESCENE = 2
    SCORESCENE = 3
    SELECTIONSCENE = 4