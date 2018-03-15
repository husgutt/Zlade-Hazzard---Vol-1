from ..gamestate import GameState
import pygame as pg
from settings import *
import json
from os import path
from os import listdir

game_folder = path.dirname(path.dirname(path.dirname(__file__)))
save_folder = path.join(game_folder, "saves")

class LoadGame(GameState):
    def __init__(self):
        super(LoadGame, self).__init__()
        self.title = self.font.render(TITLE, True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.title_rect.center = (WIDTH / 2, HEIGHT / 4)
        self.persist = {}
        self.next_state = "INTRO_LEVEL_1"
        self.load_selected = 0
        self.load_list = listdir(save_folder)
        print(self.load_list)

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "INTRO_LEVEL_1"
            self.done = True

        if keystate[pg.K_UP]:
            if self.load_selected == 0:
                self.load_selected = len(self.load_list) -1
            else:
                self.load_selected -= 1
        if keystate[pg.K_DOWN]:
            if self.load_selected == len(self.load_list) -1:
                self.load_selected = 0
            else:
                self.load_selected += 1

        if keystate[pg.K_RETURN]:
            data = json.load(open(path.join(save_folder, self.load_list[self.load_selected])))
            self.persist = data
            self.next_state = "INTRO_LEVEL_1"
            self.done = True


    def draw(self, surface):
        surface.fill(pg.Color("black"))

        for i in range(len(self.load_list)):
            if i == self.load_selected:
                button = self.font.render(self.load_list[i], True, pg.Color("red"))
            else:
                button = self.font.render(self.load_list[i], True, pg.Color("dodgerblue"))
            button_rect = button.get_rect(center=self.screen_rect.center)
            button_rect.y = WIDTH / 2 + 40*i
            surface.blit(button, button_rect)

        surface.blit(self.title, self.title_rect)
