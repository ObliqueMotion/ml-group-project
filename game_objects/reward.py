from game_objects.cell import CellType


# Direction represents the four options that the snake has to move in.
class reward():
    empty = None
    snake = None
    apple = None

    def __init__(self):
        self.empty = 0
        self.snake = -1
        self.apple = 50

    # type_of_cell describes the type of cell that the snake head is at now
    def get_reward(self, type_of_cell):
        if type_of_cell == CellType.snake:
            return self.snake
        elif type_of_cell == CellType.apple:
            return self.apple
        else:
            return self.empty
