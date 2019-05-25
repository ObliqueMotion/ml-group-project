from game_objects.square import Square


class Grid:
    unit_size = 20
    x_units = 40
    y_units = 30
    squares = None

    def __init__(self, **kwargs):
        if 'unit_size' in kwargs:
            self.unit_size = kwargs.pop('unit_size', False)
        if 'length' in kwargs:
            self.x_units = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.y_units = kwargs.pop('height', False)
        row = [Square.empty] * self.x_units
        self.squares = []
        for _ in range(0, self.y_units - 1):
            self.squares.append(row.copy())


    def render(self):
        self.squares[2][5] = Square.snake
        self.squares[2][6] = Square.snake
        self.squares[3][6] = Square.snake
        self.squares[3][7] = Square.snake
        self.squares[3][8] = Square.snake
        self.squares[3][9] = Square.snake
        self.squares[3][10] = Square.snake
        self.squares[3][13] = Square.apple

    def square(self, x, y):
        return self.squares[y][x]