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
dimensions = [13, 900, 600, 300, 30, 4]
# learning rate of split-brain neural network
learning_rate=0.01

if __name__ == "__main__":
    window = GameWindow(
        cell_size=cell_size,
        length=length,
        height=height,
        speed=speed,
        dqn_dimensions=dimensions,
        dqn_lr=learning_rate
    )
    window.play_DQN_game()