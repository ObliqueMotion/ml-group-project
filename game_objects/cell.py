from enum import Enum


# CellType represents any state that a game cell can be.
class CellType(Enum):
    empty = 0
    snake = 1
    apple = 2
