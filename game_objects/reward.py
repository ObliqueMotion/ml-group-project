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
    # TODO: return reward of +1 if snake moved closer to apply, -1 if it moved further away
    # Use manhattan distance, which eric already implemented in poximity_to_apple in grid.py
    # for this, Also possibly a greater penalty for the snake
    def get_reward(self, type_of_cell):
        if type_of_cell == CellType.snake:
            return self.snake
        elif type_of_cell == CellType.apple:
            return self.apple
