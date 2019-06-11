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
    apple_location = None
    cell_size = None
    length = None
    height = None
    cells = None
    snake = None
    rewards = None

    def __init__(self, **kwargs):
        """Creates a new 2D grid of cells and adds a random Snake and a random apple."""
        if 'cell_size' in kwargs:
            self.cell_size = kwargs.pop('cell_size', False)
        if 'length' in kwargs:
            self.length = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.height = kwargs.pop('height', False)

        row = [CellType.empty] * self.length
        self.cells = []
        for _ in range(0, self.height):
            self.cells.append(row.copy())

        start_direction = random.choice(list(Direction))
        snake_x = random.randint(3, self.length - 4)
        snake_y = random.randint(3, self.height - 4)

        self.snake = Snake(x=snake_x, y=snake_y, direction=start_direction)

        for cell in self.snake.body:
            self.set_cell(cell, CellType.snake)

        self.generate_new_apple()

    def generate_new_apple(self):
        """Generates a new apple in a random position that is not in the Snake or in another apple"""
        x = random.randint(0, self.length - 1)
        y = random.randint(0, self.height - 1)
        cell = [x, y]

        while cell in self.snake.body or self.get_cell(x, y) is CellType.apple:
            x = random.randint(0, self.length - 1)
            y = random.randint(0, self.height - 1)
            cell = [x, y]

        self.set_cell(cell, CellType.apple)
        self.apple_location = cell

    def next_frame(self):
        """Updates the Grid state based on the Snake's new position."""
        got_apple = False
        popped_cell = self.snake.advance()
        if self.snake_died():
            return
        (new_x, new_y) = self.snake.head()

        if popped_cell is not None:
            self.set_cell(popped_cell, CellType.empty)

        if self.get_cell(new_x, new_y) == CellType.apple:
            got_apple = True
            self.snake.grow()
            self.generate_new_apple()

        self.set_cell(self.snake.head(), CellType.snake)

        return got_apple

    def get_cell(self, x, y):
        """Returns the cell at the given (x, y) location."""
        return self.cells[y][x]

    def set_cell(self, cell, cell_type):
        """Sets a cell to a new value."""
        x = cell[__X__]
        y = cell[__Y__]
        self.cells[y][x] = cell_type

    def change_direction(self, direction):
        """Changes the snake's direction to a new direction."""
        self.snake.direction = direction

    def snake_died(self):
        """Checks to see if the snake is dead."""
        (x, y) = self.snake.head()
        return (
            self.snake.head() in self.snake.tail()
            or not (0 <= x < self.length)
            or not (0 <= y < self.height)
        )

    def safe_cells(self, direction):
        if direction == Direction.up:
            return self.safe_cells_up()
        elif direction == Direction.down:
            return self.safe_cells_down()
        elif direction == Direction.left:
            return self.safe_cells_left()
        else:
            return self.safe_cells_right()

    def safe_cells_up(self):
        """Returns the percentage of safe cells directly above the Snake's head relative to the snake's location."""
        (x, y) = self.snake.head()
        max_dist = y
        y -= 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            y -= 1
        if max_dist == 0 or count == 0:
            return -1.0
        else:
            return float(count) / float(max_dist)

    def safe_cells_down(self):
        """Returns the percentage of safe cells directly below the Snake's head relative to the snake's location."""
        (x, y) = self.snake.head()
        max_dist = self.height - y - 1
        y += 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            y += 1
        if max_dist == 0 or count == 0:
            return -1.0
        else:
            return float(count) / float(max_dist)

    def safe_cells_left(self):
        """Returns the percentage of safe cells directly to the left of the Snake's head relative to the snake's location."""
        (x, y) = self.snake.head()
        max_dist = x
        x -= 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            x -= 1
        if max_dist == 0 or count == 0:
            return -1.0
        else:
            return float(count) / float(max_dist)

    def safe_cells_right(self):
        """Returns the percentage of safe cells directly to the right of the Snake's head relative to the snake's location."""
        (x, y) = self.snake.head()
        max_dist = self.length - x - 1
        x += 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            x += 1
        if max_dist == 0 or count == 0:
            return -1.0
        else:
            return float(count) / float(max_dist)

    def safe_cells_up_global(self):
        """Returns the percentage of safe cells directly above the Snake's head relative to the board size."""
        (x, y) = self.snake.head()
        y -= 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            y -= 1
        if count == 0:
            return -1.0
        else:
            return float(count) / float(self.height)

    def safe_cells_down_global(self):
        """Returns the percentage of safe cells directly below the Snake's head relative to the board size."""
        (x, y) = self.snake.head()
        y += 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            y += 1
        if count == 0:
            return -1.0
        else:
            return float(count) / float(self.height)

    def safe_cells_left_global(self):
        """Returns the percentage of safe cells directly to the left of the Snake's head relative to the board size."""
        (x, y) = self.snake.head()
        x -= 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            x -= 1
        if count == 0:
            return -1.0
        else:
            return float(count) / float(self.length)

    def safe_cells_right_global(self):
        """Returns the percentage of safe cells directly to the right of the Snake's head relative to the board size."""
        (x, y) = self.snake.head()
        x += 1
        count = 0
        while(x in range(0, self.length) and y in range(0, self.height)):
            if self.get_cell(x, y) is CellType.snake and count < self.snake.dist_from_tail(x, y):
                break
            count += 1
            x += 1
        if count == 0:
            return -1.0
        else:
            return float(count) / float(self.length)

    # Uses Manhattan Distance
    def proximity_to_apple(self):
        """Returns the snake's closeness to the apple as a percentage of the max possible distance it could be."""
        (snake_x, snake_y) = self.snake.head()
        (apple_x, apple_y) = self.apple_location

        farthest_x_dist = max(apple_x, self.length - apple_x)
        farthest_y_dist = max(apple_y, self.height - apple_y)

        actual_x_dist = abs(snake_x - apple_x)
        actual_y_dist = abs(snake_y - apple_y)

        return 1.0 - float(actual_x_dist + actual_y_dist) / float(farthest_x_dist + farthest_y_dist)

    def apple_is_up(self):
        """Returns 1.0 if the apple is above the snake, otherwise 0.0"""
        (_, snake_y) = self.snake.head()
        (_, apple_y) = self.apple_location
        return float(apple_y < snake_y)

    def apple_is_down(self):
        """Returns 1.0 if the apple is below the snake, otherwise 0.0"""
        (_, snake_y) = self.snake.head()
        (_, apple_y) = self.apple_location
        return float(apple_y > snake_y)

    def apple_is_left(self):
        """Returns 1.0 if the apple is to the left of the snake, otherwise 0.0"""
        (snake_x, _) = self.snake.head()
        (apple_x, _) = self.apple_location
        return float(apple_x < snake_x)

    def apple_is_right(self):
        """Returns 1.0 if the apple is to the right of the snake, otherwise 0.0"""
        (snake_x, _) = self.snake.head()
        (apple_x, _) = self.apple_location
        return float(apple_x > snake_x)

    def apple_is_up_safe(self, threshold):
        """Returns 1.0 if the apple is above the snake and the number of safe cells is above threshold, otherwise 0.0"""
        (_, snake_y) = self.snake.head()
        (_, apple_y) = self.apple_location
        if apple_y < snake_y and self.safe_cells_up() > threshold:
            return 1.0
        else:
            return 0.0

    def apple_is_down_safe(self, threshold):
        """Returns 1.0 if the apple is below the snake and the number of safe cells is above threshold, otherwise 0.0"""
        (_, snake_y) = self.snake.head()
        (_, apple_y) = self.apple_location
        if apple_y > snake_y and self.safe_cells_down() > threshold:
            return 1.0
        else:
            return 0.0

    def apple_is_left_safe(self, threshold):
        """Returns 1.0 if the apple is to the left of the snake and the number of safe cells is above threshold, otherwise 0.0"""
        (snake_x, _) = self.snake.head()
        (apple_x, _) = self.apple_location
        if apple_x < snake_x and self.safe_cells_left() > threshold:
            return 1.0
        else:
            return 0.0

    def apple_is_right_safe(self, threshold):
        """Returns 1.0 if the apple is to the right of the snake and the number of safe cells is above threshold, otherwise 0.0"""
        (snake_x, _) = self.snake.head()
        (apple_x, _) = self.apple_location
        if apple_x > snake_x and self.safe_cells_right() > threshold:
            return 1.0
        else:
            return 0.0
