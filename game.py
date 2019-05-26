from game_objects.window import GameWindow

# cell_size = square pixels per cell
# length = number of cells per row in GameWindow
# height = number of cells per column in GameWindow
# speed = speed of the game (actions per second)
if __name__ == "__main__":
    window = GameWindow(cell_size=60, length=32, height=16, speed=10)
    window.run_game_loop()