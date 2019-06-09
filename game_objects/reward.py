from enum import Enum


# Direction represents the four options that the snake has to move in.
class reward(Enum):
    empty = 0
    snake = -1
    apple = 50
