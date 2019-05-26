import pygame as pg
from pygame.locals import *
from pygame.color import Color
from game_objects.grid import Grid
from game_objects.cell import CellType
from game_objects.direction import Direction

__SNAKE_CELL_PATH__ = "images/white_square.png"
__APPLE_CELL_PATH__ = "images/green_square.png"


# The GameWindow is responsible for running the main game loop.
# The GameWindow is responsible for drawing the game state to the screen.
class GameWindow:
    grid = None
    clock = None
    height = None
    length = None
    surface = None
    cell_size = None
    actions_per_second = None

    def __init__(self, **kwargs):
        """Initializes the game window."""
        pg.init()
        pg.display.set_caption('Snake')
        self.clock = pg.time.Clock()
        if 'cell_size' in kwargs:
            self.cell_size = kwargs.pop('cell_size', False)
        if 'length' in kwargs:
            self.length = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.height = kwargs.pop('height', False)
        if 'speed' in kwargs:
            self.actions_per_second = kwargs.pop('speed', False)
        self._exit = False

    def reset(self, **kwargs):
        """Resets the game state with a new snake and apple in random positions."""
        pg.display.set_caption('Snake')

        self._surface = pg.display.set_mode(
            (self.length * self.cell_size, self.height * self.cell_size), 
            pg.HWSURFACE
        )
        self.grid = Grid(
            cell_size=self.cell_size,
            length=self.length,
            height=self.height
        )
        self.snake_cell_image = pg.image.load(__SNAKE_CELL_PATH__).convert()
        self.snake_cell_image = pg.transform.scale(
            self.snake_cell_image,
            (self.cell_size, self.cell_size)
        ).convert()

        self.apple_cell_image = pg.image.load(
            __APPLE_CELL_PATH__
        ).convert()

        self.apple_cell_image = pg.transform.scale(
            self.apple_cell_image, (self.cell_size, self.cell_size)).convert_alpha()

        self._exit = False

    def check_for_exit(self):
        """Checks if the user has decided to exit."""
        keys = pg.key.get_pressed()
        if (keys[K_ESCAPE]):
            self._exit = True
        for event in pg.event.get():
            if event.type == QUIT:
                self._exit = True

    # TODO: Add inputs from ML models.
    def handle_input(self):
        """Checks for input to the game."""
        keys = pg.key.get_pressed()

        if (keys[K_UP]):
            self.grid.change_direction(Direction.up)
        if (keys[K_DOWN]):
            self.grid.change_direction(Direction.down)
        if (keys[K_LEFT]):
            self.grid.change_direction(Direction.left)
        if (keys[K_RIGHT]):
            self.grid.change_direction(Direction.right)
        if (keys[K_SPACE]):
            self.grid.snake.grow()

    def perform_actions(self):
        """Executes all relevant game-state changes."""
        self.grid.next_frame()

    def render(self):
        """Draws the changes to the game-state (if any) to the screen."""
        self._surface.fill(Color('black'))
        for y in range(0, self.height):
            for x in range(0, self.length):
                if self.grid.get_cell(x, y) == CellType.snake:
                    self._surface.blit(self.snake_cell_image,
                                       (x * self.cell_size, y * self.cell_size))
                elif self.grid.get_cell(x, y) == CellType.apple:
                    self._surface.blit(self.apple_cell_image,
                                       (x * self.cell_size, y * self.cell_size))
        pg.display.update()

    def cleanup(self):
        """Quits pygame."""
        pg.quit()

    # TODO: Add win condition.
    def check_for_end_game(self):
        """Checks to see if the snake has died."""
        if self.grid.snake_died():
            self.reset()

    def output_to_console(self):
            vert = None
            horiz = None
            if self.grid.food_is_up():
                vert = "Up  "
            elif self.grid.food_is_down():
                vert = "Down"
            else:
                vert = "None"
            if self.grid.food_is_left():
                horiz = "Left "
            elif self.grid.food_is_right():
                horiz = "Right"
            else:
                horiz = "None "
            print(
                "Apple is: (", vert, ",", horiz,
                ")\tProximity: ",
                str(round(self.grid.distance_from_apple(), 2)), "\t[x, y]:",
                self.grid.snake.head(),
                "   \tSafeUp:", str(round(self.grid.safe_cells_up(), 2)),
                "    \tSafeDown:", str(round(self.grid.safe_cells_down(), 2)),
                "  \tSafeLeft:", str(round(self.grid.safe_cells_left(), 2)),
                "  \tSafeRight:", str(round(self.grid.safe_cells_right(), 2)),
            )

    def run_game_loop(self):
        """Runs the main game loop."""
        if self.reset() == False:
            self._exit = True
        while(not self._exit):
            pg.event.pump()
            self.clock.tick(self.actions_per_second)
            self.check_for_exit()
            self.handle_input()
            self.perform_actions()
            self.check_for_end_game()
            self.render()
            self.output_to_console()

        self.cleanup()
