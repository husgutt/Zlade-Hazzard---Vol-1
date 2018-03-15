from ..gamestate import GameState
import pygame as pg
from settings import *
import tools.textrectexception as tre

class IntroLevel1(GameState):
    def __init__(self):
        super(IntroLevel1, self).__init__()
        self.persist = {}

        self.output = ""
        self.count = 0
        self.delay = 0
        self.message_number = 0
        self.message = ["Hei din fjomp, vil du gå videre? Trykk enter da...",
                        "Veldig bra jobba! Imponerende. Du er god til å trykke på knapper",
                        "Det kommer godt med.",
                        "Trykk... trykk.... trykk...",
                        "ÅÅåå så flink!",
                        "Er mamma stolt?"]
        self.blink_active = False
        self.blink_delay = 0
        self.blink = None



    def startup(self, persistent):
        self.persist = persistent
        self.title = self.font.render(self.persist['player'], True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.font = pg.font.Font(None, 22)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "GLOBAL_MAP"
            self.done = True
        if keystate[pg.K_RETURN]:
            if self.count >= len(self.message[self.message_number]):
                self.count = 0
                self.message_number += 1
            else:
                 self.count = len(self.message[self.message_number])-1
            if self.message_number == len(self.message):
                self.next_state = "GLOBAL_MAP"
                self.message_number = 0
                self.done = True

    def update(self, dt):
        self.delay += dt
        if self.count <= len(self.message[self.message_number]) and self.delay > 50 :
            self.output = self.message[self.message_number][0:self.count]
            self.count += 1
            self.delay = 0
        self.blink_delay += dt
        if self.blink_delay > 300:
            self.blink_active = not self.blink_active
            self.blink_delay = 0



    def draw(self, surface):
        # self.info = self.font.render(self.output, True, pg.Color("dodgerblue"))
        self.info_rect = pg.Rect((0, HEIGHT * 3 / 4, WIDTH, HEIGHT / 4))
        self.blink_rect = pg.Rect((WIDTH*3 / 4, HEIGHT - 40, 10, 10))
        self.info = tre.render_textrect(self.output, self.font, self.info_rect, (255, 0, 0), (0, 255, 0), 1)
        # self.info_rect = self.info.get_rect(center=self.screen_rect.center)
        # self.info_rect.y = WIDTH*3/4
        surface.fill(pg.Color("black"))
        surface.blit(self.title, self.title_rect)
        surface.blit(self.info, self.info_rect)
        if self.blink_active and self.count == len(self.message[self.message_number]):
            self.blink = tre.render_textrect("", self.font, self.blink_rect, (0, 0, 0), (255, 255, 255), 1)
            surface.blit(self.blink, self.blink_rect)
