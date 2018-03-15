from ..gamestate import GameState
import pygame as pg
from settings import *

class SplashScreen(GameState):
    def __init__(self):
        super(SplashScreen, self).__init__()
        self.title = self.font.render(TITLE, True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.title_rect.center = (WIDTH / 2, HEIGHT / 4)
        self.persist = {}
        self.next_state = "INTRO_LEVEL_1"
        self.menu_choices = ["START NEW GAME", "LOAD GAME", "SETTINGS", "EXIT GAME"]
        self.menu_selected = 0

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "INTRO_LEVEL_1"
            self.done = True

        if keystate[pg.K_UP]:
            if self.menu_selected == 0:
                self.menu_selected = len(self.menu_choices) -1
            else:
                self.menu_selected -= 1
        if keystate[pg.K_DOWN]:
            if self.menu_selected == len(self.menu_choices) -1:
                self.menu_selected = 0
            else:
                self.menu_selected += 1

        if keystate[pg.K_RETURN]:
            if self.menu_selected == 0:
                self.next_state = "NEWGAME"
                self.done = True
            if self.menu_selected == 1:
                self.next_state = "LOADGAME"
                self.done = True
            if self.menu_selected == 2:
                self.next_state = "INTRO_LEVEL_1"
                self.done = True
            if self.menu_selected == 3:
                self.quit = True

    def draw(self, surface):
        surface.fill(pg.Color("black"))

        for i in range(len(self.menu_choices)):
            if i == self.menu_selected:
                button = self.font.render(self.menu_choices[i], True, pg.Color("red"))
            else:
                button = self.font.render(self.menu_choices[i], True, pg.Color("dodgerblue"))
            button_rect = button.get_rect(center=self.screen_rect.center)
            button_rect.y = WIDTH / 2 + 40*i
            surface.blit(button, button_rect)

        surface.blit(self.title, self.title_rect)
