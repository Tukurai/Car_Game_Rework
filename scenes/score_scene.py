from scenes.scene_base import SceneBase


class ScoreScene(SceneBase):
    '''The score scene, this is where the player will see their score, and other highscores.'''
    def __init__(self):
        super().__init__()
        self.name = "score_scene"

        # Notify that the scene is initialized
        self.events.on_scene_initialized.notify()

    def handle_event(self, event):
        super().handle_event(event)

    def update(self, timedelta, input_state):
        super().update(timedelta, input_state)

    def draw(self, screen):
        super().draw(screen)