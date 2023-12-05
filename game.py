from core.dependency_injection import DI
from core.game_engine import GameEngine


if __name__ == "__main__":
    injector = DI()
    game_engine = injector.get(GameEngine)
    game_engine.run_game_loop()
