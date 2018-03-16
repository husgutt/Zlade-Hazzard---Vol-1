from ..gamestate import GameState
import pygame as pg
from settings import *
from sprites import *
import json
from os import path

game_folder = path.dirname(path.dirname(path.dirname(__file__)))
save_folder = path.join(game_folder, "saves")

class NewGame(GameState):
    def __init__(self):
        super(NewGame, self).__init__()
        self.title = self.font.render("START NEW GAME", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.title_rect.center = (WIDTH / 2, HEIGHT / 4)
        self.persist = {}
        self.next_state = "INTRO_LEVEL_1"

        self.input_box = pg.Rect(WIDTH / 2, HEIGHT / 2, 140, 32)
        self.input_box.center = (WIDTH / 2, HEIGHT / 2)
        self.color_inactive = pg.Color('lightskyblue3')
        self.color_active = pg.Color('dodgerblue2')
        self.color = self.color_inactive
        self.active = False
        self.text = ''

        self.background = pg.image.load(path.join(IMG_FOLDER, STARTSCREEN)).convert()
        self.background =  pg.transform.scale(self.background, (HEIGHT, HEIGHT))
        self.background_rect = self.background.get_rect()
        self.background_rect.x = -40


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "INTRO_LEVEL_1"
            self.done = True

        if event.type == pg.MOUSEBUTTONDOWN:
                # If the user clicked on the input_box rect.
                if self.input_box.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active = not self.active
                else:
                    self.active = False
                # Change the current color of the input box.
                self.color = self.color_active if self.active else self.color_inactive
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    with open(path.join(save_folder, self.text+'-save.txt'), 'w') as file:
                        self.persist['player'] = self.text
                        self.persist["animate_on_map"] = True
                        self.persist["cleared_level"] = 0
                        file.write(json.dumps(self.persist))
                    self.next_state = "INTRO_LEVEL_1"
                    self.done = True
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode

    def update(self, dt):
        self.text_box = self.font.render("TEST", True, pg.Color("dodgerblue"))

    def draw(self, surface):
        surface.fill(pg.Color("black"))
        surface.blit(self.background, self.background_rect)

        # for i in range(len(self.menu_choices)):
        #     if i == self.menu_selected:
        #         button = self.font.render(self.menu_choices[i], True, pg.Color("red"))
        #     else:
        #         button = self.font.render(self.menu_choices[i], True, pg.Color("dodgerblue"))
        #     button_rect = button.get_rect(center=self.screen_rect.center)
        #     button_rect.y = WIDTH / 2 + 40*i

        txt_surface = self.font.render(self.text, True, self.color)
        width = max(200, txt_surface.get_width()+10)
        self.input_box.w = width
        # Blit the text.
        surface.blit(txt_surface, (self.input_box.x+5, self.input_box.y+5))
        # Blit the input_box rect.
        pg.draw.rect(surface, self.color, self.input_box, 2)
        surface.blit(self.title, self.title_rect)
