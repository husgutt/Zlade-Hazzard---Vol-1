import pygame as pg
from settings import *

class Tools():
    def __init__(self):
        self.font_name = pg.font.match_font('arial')

    def draw_text(self, surf, text, size, x, y):
        font = pg.font.Font(self.font_name, size)
        text_surface = font.render(text, True, WHITE)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        surf.blit(text_surface, text_rect)

    def draw_shield_bar(self, surf, x, y, pct):
        if pct < 0:
            pct = 0
        BAR_LENGTH = 100
        BAR_HEIGHT = 10
        fill = (pct / 100) * BAR_LENGTH
        outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
        fill_rect = pg.Rect(x, y, fill, BAR_HEIGHT)
        pg.draw.rect(surf, GREEN, fill_rect)
        pg.draw.rect(surf, WHITE, outline_rect, 2)

    def draw_lives(self, surf, x, y, lives, img):
        for i in range(lives):
            img_rect = img.get_rect()
            img_rect.x = x + 30*i
            img_rect.y = y
            img.set_colorkey(BLACK)
            surf.blit(img, img_rect)
