import pygame as pg
from pygame.locals import *
from pygame.color import Color

class GameWindow:
    width = 800
    height = 600
    actions_per_second = 60
    clock = pg.time.Clock()

    def __init__(self):
        self._exit = False
        self._display = None

    def init(self):
        pg.init()
        pg.display.set_caption('Snake')
        self._display = pg.display.set_mode((self.width ,self.height), pg.HWSURFACE)
        self._exit = False
 
    def check_for_exit(self):
        keys = pg.key.get_pressed() 
        if (keys[K_ESCAPE]):
            self._exit = True
    
    def render(self):
        self.clock.tick(self.actions_per_second)
        self._display.fill(Color('black'))
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