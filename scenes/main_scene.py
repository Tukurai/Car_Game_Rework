from scenes.scene_base import SceneBase


class MainScene(SceneBase):
    '''The main scene, the first scene to be shown when the game starts.'''
    def __init__(self):
        super().__init__()
        self.name = "main_scene"

        # Notify that the scene is initialized
        self.events.on_scene_initialized.notify()

    def handle_event(self, event):
        super().handle_event(event)

    def update(self, timedelta, input_state):
        super().update(timedelta, input_state)

    def draw(self, screen):
        super().draw(screen)