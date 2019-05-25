import pygame as pg
from game_objects.grid import Grid
from game_objects.square import Square
from pygame.locals import *
from pygame.color import Color

__SNAKE_SQUARE_PATH__ = "images/white_square.png"
__APPLE_SQUARE_PATH__ = "images/green_square.png"

class GameWindow:
    unit_size = None
    length = None
    height = None
    actions_per_second = None
    grid = None
    clock = pg.time.Clock()

    def __init__(self, **kwargs):
        pg.display.set_caption('Snake')
        if 'unit_size' in kwargs:
            self.unit_size = kwargs.pop('unit_size', False)
        if 'length' in kwargs:
            self.length = kwargs.pop('length', False)
        if 'height' in kwargs:
            self.height = kwargs.pop('height', False)
        if 'aps' in kwargs:
            self.actions_per_second = kwargs.pop('aps', False)
        self._exit = False
        self._surface = None

    def init(self, **kwargs):
        pg.init()
        pg.display.set_caption('Snake')
        self._surface = pg.display.set_mode((self.length * self.unit_size ,self.height * self.unit_size), pg.HWSURFACE)
        self.grid = Grid(unit_size = self.unit_size, length = self.length, height = self.height, pg = pg)
        self.snake_square_image = pg.image.load(__SNAKE_SQUARE_PATH__).convert()
        self.snake_square_image = pg.transform.scale(self.snake_square_image, (self.unit_size, self.unit_size)).convert()
        self.apple_square_image = pg.image.load(__APPLE_SQUARE_PATH__).convert_alpha()
        self.apple_square_image = pg.transform.scale(self.apple_square_image, (self.unit_size, self.unit_size)).convert_alpha()
        self._exit = False
 
    def check_for_exit(self):
        keys = pg.key.get_pressed() 
        if (keys[K_ESCAPE]):
            self._exit = True
        for event in pg.event.get():
            if event.type == QUIT:
                self._exit = True
    
    def render(self):
        self.clock.tick(self.actions_per_second)
        self._surface.fill(Color('black'))
        self.grid.render()
        for y in range(0, self.height - 1):
            for x in range(0, self.length - 1):
                if self.grid.square(x, y) == Square.snake:
                    self._surface.blit(self.snake_square_image, (x * self.unit_size, y * self.unit_size))
                elif self.grid.square(x, y) == Square.apple:
                    self._surface.blit(self.apple_square_image, (x * self.unit_size, y * self.unit_size))
        pg.display.update()
 
    def cleanup(self):
        pg.quit()
 
    def run_game_loop(self):
        if self.init() == False:
            self._exit = True
 
        while( not self._exit ):
            pg.event.pump()
            self.check_for_exit()
            self.render()
        self.cleanup()