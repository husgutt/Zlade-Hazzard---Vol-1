from .gamestate import GameState
import pygame as pg
from settings import *
from os import path
import json

game_folder = path.dirname(path.dirname(__file__))
save_folder = path.join(game_folder, "saves")

class ScoreScreen(GameState):
    def __init__(self):
        super(ScoreScreen, self).__init__()
        self.title = self.font.render("SCORE SCREEN", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist = {}

    def startup(self, persistent):
        self.persist = persistent

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_RETURN]:
            player_name = self.persist['player']
            with open(path.join(save_folder, player_name+'-save.txt'), 'w') as file:
                file.write(json.dumps(self.persist))


            self.next_state = "OUTRO_LEVEL_1"
            self.done = True

    def draw(self, surface):
        cleared_level = self.persist['cleared_level']
        score = self.persist['cleared_level_score']
        score_string = "Score: " + str(score)
        score_text = self.font.render(score_string, True, pg.Color("dodgerblue"))
        score_rect = score_text.get_rect(center=(WIDTH/2,HEIGHT / 4))
        surface.blit(self.title, self.title_rect)
        surface.blit(score_text, score_rect)
