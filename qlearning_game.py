import random
from game_objects.window import GameWindow

# cell_size = square pixels per cell
# length = number of cells per row in GameWindow
# height = number of cells per column in GameWindow
# speed = speed of the game (actions per second)
if __name__ == "__main__":
    random.seed()
    window = GameWindow(cell_size=20, length=20, height=20, speed=20)
    window.play_QLEARN_game()
