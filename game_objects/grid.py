import random
from game_objects.snake import Snake
from game_objects.cell import CellType
from game_objects.direction import Direction

__X__ = 0
__Y__ = 1

# Grid is the central controller of the game.
# The Grid maintains the location of the snake and the apple.
# The Grid informs the GameWindow what to draw to the screen.
class Grid:
    cell_size = None
    x_cells = None
    y_cells = None
    cells = None
    snake = None

    def __init__(self, **kwargs):
        """Creates a new 2D grid of cells and adds a random Snake and a random apple."""
        if 'cell_size' in kwargs:
            self.cell_size = kwargs.pop('cell_size', False)
        if 'length' in kwargs:
            self.x_cells = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.y_cells = kwargs.pop('height', False)

        row = [CellType.empty] * self.x_cells
        self.get_cells = []
        for _ in range(0, self.y_cells):
            self.get_cells.append(row.copy())

        print(len(self.get_cells))
        print(len(self.get_cells[0]))

        start_direction = random.choice(list(Direction))
        snake_x = random.randint(0, self.x_cells - 1)
        snake_y = random.randint(0, self.y_cells - 1)

        self.snake = Snake(x=snake_x, y=snake_y, direction=start_direction)
        self.set_cell([snake_x, snake_y], CellType.snake)
        self.generate_new_apple()

    def generate_new_apple(self):
        """Generates a new apple in a random position that is not in the Snake or in another apple"""
        x = random.randint(0, self.x_cells - 1)
        y = random.randint(0, self.y_cells - 1)
        cell = [x, y]
        while cell in self.snake.body or self.get_cell(x, y) is CellType.apple:
            x = random.randint(0, self.x_cells - 1)
            y = random.randint(0, self.y_cells - 1)
            cell = [x, y]
        print("NEW APPLE")
        print(cell)
        self.set_cell(cell, CellType.apple)
        print("NEW APPLE")

    def next_frame(self):
        """Updates the Grid state based on the Snake's new position."""
        popped_cell = self.snake.advance()
        if self.snake_died():
            return

        (new_x, new_y) = self.snake.head()
        print((new_x, new_y))

        if popped_cell is not None:
            self.set_cell(popped_cell, CellType.empty)
        if self.get_cell(new_x, new_y) == CellType.apple:
            self.snake.grow()
            self.generate_new_apple()
        self.set_cell(self.snake.head(), CellType.snake)

    def get_cell(self, x, y):
        """Returns the cell at the given (x, y) location."""
        return self.get_cells[y][x]

    def set_cell(self, cell, cell_type):
        """Sets a cell to a new value."""
        x = cell[__X__]
        y = cell[__Y__]
        self.get_cells[y][x] = cell_type

    def change_direction(self, direction):
        """Changes the snake's direction to a new direction."""
        self.snake.direction = direction

    def snake_died(self):
        """Checks to see if the snake is dead."""
        (x, y) = self.snake.head()
        return (self.snake.head() in self.snake.tail()) or (x < 0 or self.x_cells <= x) or (y < 0 or self.y_cells <= y)
