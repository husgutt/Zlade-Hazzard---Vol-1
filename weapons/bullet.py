import pygame as pg
from math import radians, degrees, cos, sin
from settings import *
from os import path

class Bullet(pg.sprite.Sprite):

    def __init__(self, x, y, deg, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.bullet_img = self.game.ll.weapons[0]
        self.deg = radians(deg)
        self.image = pg.transform.rotate(self.bullet_img, degrees(self.deg)-90)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x + (self.bullet_img.get_size()[1] / 2) * cos(self.deg)
        self.speedy = -10*sin(self.deg)
        self.speedx = 10*cos(self.deg)
        print(sin(90-self.deg))

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy

        if self.rect.bottom < 0:
            self.kill()
