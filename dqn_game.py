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
# the number of states to collect in replay memory before updating.
batch_size = 100
# the number of samples to draw from the batch during training.
sample_size = 40

if __name__ == "__main__":
    window = GameWindow(
        cell_size=cell_size,
        length=length,
        height=height,
        speed=speed,
        dqn_dimensions=dimensions,
        dqn_lr=learning_rate,
        dqn_batch_size=batch_size,
        dqn_sample_size=sample_size
    )
    window.play_DQN_game()