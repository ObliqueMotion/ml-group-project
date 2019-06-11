from game_objects.window import GameWindow


# square pixels per cell
cell_size = 20
# number of cells per row in GameWindow
length = 40
# number of cells per column in GameWindow
height = 30
# speed of the game (actions per second)
speed = 20

if __name__ == "__main__":
    window = GameWindow(
        cell_size=cell_size,
        length=length,
        height=height,
        speed=speed
    )
    window.play_keyboard_input_game()
