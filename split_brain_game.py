from game_objects.window import GameWindow


# square pixels per cell
cell_size = 20
# number of cells per row in GameWindow
length = 40
# number of cells per column in GameWindow
height = 30
# speed of the game (actions per second)
speed = 20
# dimensions of split-brain neural network
dimensions = [4, 1000, 100, 10, 1]
# learning rate of split-brain neural network
learning_rate=0.01

if __name__ == "__main__":
    window = GameWindow(
        cell_size=cell_size,
        length=length,
        height=height,
        speed=speed,
        sb_dimensions=dimensions,
        sb_lr=learning_rate
    )
    window.play_split_brain_network_game()