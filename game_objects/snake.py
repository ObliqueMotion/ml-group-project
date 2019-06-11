from game_objects.direction import Direction

__X__ = 0
__Y__ = 1
__LAST__ = -1


# The Snake is a wrapper around a queue of (x, y) pairs.
# The Snake's (x, y) pairs inform the Grid where to draw the Snake.
class Snake:
    body = None
    direction = None
    increase_length = None

    def __init__(self, **kwargs):
        if 'x' in kwargs and 'y' in kwargs and 'direction' in kwargs:
            x = kwargs.pop('x', False)
            y = kwargs.pop('y', False)
            self.direction = kwargs.pop('direction', False)
            if self.direction == Direction.up:
                self.body = [[x, y + 2], [x, y + 1], [x, y]]
            elif self.direction == Direction.down:
                self.body = [[x, y - 2], [x, y - 1], [x, y]]
            elif self.direction == Direction.left:
                self.body = [[x + 2, y], [x + 1, y], [x, y]]
            elif self.direction == Direction.right:
                self.body = [[x - 2, y], [x - 1, y], [x, y]]

        self.increase_length = False

    def advance(self):
        """Advances the snake to the next cell in the direction the snake is going."""
        next_cell = self.body[__LAST__].copy()
        popped_cell = None
        if self.direction == Direction.up:
            next_cell[__Y__] -= 1
            self.body.append(next_cell.copy())
        elif self.direction == Direction.down:
            next_cell[__Y__] += 1
            self.body.append(next_cell.copy())
        elif self.direction == Direction.left:
            next_cell[__X__] -= 1
            self.body.append(next_cell.copy())
        elif self.direction == Direction.right:
            next_cell[__X__] += 1
            self.body.append(next_cell.copy())

        if self.increase_length:
            self.increase_length = False
        else:
            popped_cell = self.body.pop(0)

        return popped_cell

    def grow(self):
        """The snake will grow longer upon its next advance."""
        self.increase_length = True

    def head(self):
        """Returns the head (x, y) pair of the Snake"""
        return self.body[__LAST__]

    def tail(self):
        """All (x, y) pairs except for the head of the Snake"""
        return self.body[:__LAST__]

    def dist_from_tail(self, x, y):
        count = 0
        target = (x, y)
        for cell in self.body:
            if cell[0] == target[0] and cell[1] == target[1]:
                return count
            count += 1
        return -1

    def dir_to_int(self):
        if self.direction == Direction.up:
            return 0
        elif self.direction == Direction.down:
            return 1
        elif self.direction == Direction.left:
            return 2
        else:
            return 3
