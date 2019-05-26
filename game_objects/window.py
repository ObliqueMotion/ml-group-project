import pygame as pg
from pygame.locals import *
from pygame.color import Color
from game_objects.grid import Grid
from game_objects.cell import CellType
from game_objects.direction import Direction

__SNAKE_CELL_PATH__ = "images/white_square.png"
__APPLE_CELL_PATH__ = "images/green_square.png"

class GameWindow:
    cell_size = None
    length = None
    height = None
    actions_per_second = None
    grid = None
    clock = pg.time.Clock()

    def __init__(self, **kwargs):
        pg.init()
        pg.display.set_caption('Snake')
        if 'cell_size' in kwargs:
            self.cell_size = kwargs.pop('cell_size', False)
        if 'length' in kwargs:
            self.length = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.height = kwargs.pop('height', False)
        if 'aps' in kwargs:
            self.actions_per_second = kwargs.pop('aps', False)
        self._exit = False
        self._surface = None

    def init(self, **kwargs):
        pg.display.set_caption('Snake')
        self._surface = pg.display.set_mode((self.length * self.cell_size, self.height * self.cell_size), pg.HWSURFACE)
        self.grid = Grid(cell_size = self.cell_size, length = self.length, height = self.height)
        self.snake_cell_image = pg.image.load(__SNAKE_CELL_PATH__).convert()
        self.snake_cell_image = pg.transform.scale(self.snake_cell_image, (self.cell_size, self.cell_size)).convert()
        self.apple_cell_image = pg.image.load(__APPLE_CELL_PATH__).convert_alpha()
        self.apple_cell_image = pg.transform.scale(self.apple_cell_image, (self.cell_size, self.cell_size)).convert_alpha()
        self._exit = False
 
    def check_for_exit(self):
        keys = pg.key.get_pressed() 
        if (keys[K_ESCAPE]):
            self._exit = True
        for event in pg.event.get():
            if event.type == QUIT:
                self._exit = True

    def handle_input(self):
        keys = pg.key.get_pressed()

        if (keys[K_UP]):
            self.grid.change_direction(Direction.up)
        if (keys[K_DOWN]):
            self.grid.change_direction(Direction.down)
        if (keys[K_LEFT]):
            self.grid.change_direction(Direction.left)
        if (keys[K_RIGHT]):
            self.grid.change_direction(Direction.right)

    def perform_actions(self):
        self.grid.next_frame()

    def render(self):
        self._surface.fill(Color('black'))
        for y in range(0, self.height):
            for x in range(0, self.length):
                if self.grid.get_cell(x, y) == CellType.snake:
                    self._surface.blit(self.snake_cell_image, (x * self.cell_size, y * self.cell_size))
                elif self.grid.get_cell(x, y) == CellType.apple:
                    self._surface.blit(self.apple_cell_image, (x * self.cell_size, y * self.cell_size))
        pg.display.update()
 
    def cleanup(self):
        pg.quit()


    def check_for_end_game(self):
        if self.grid.snake_died():
            self.init()
 
    def run_game_loop(self):
        if self.init() == False:
            self._exit = True
        while( not self._exit ):
            pg.event.pump()
            self.clock.tick(self.actions_per_second)
            self.check_for_exit()
            self.handle_input()
            self.perform_actions()
            self.check_for_end_game()
            self.render()
        self.cleanup()
