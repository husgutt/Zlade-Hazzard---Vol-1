from ..gamestate import GameState
import pygame as pg
from settings import *

class OutroLevel1(GameState):
    def __init__(self):
        super(OutroLevel1, self).__init__()
        self.title = self.font.render("OutroLevel1", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist = {}

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "GLOBAL_MAP"
            self.done = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
