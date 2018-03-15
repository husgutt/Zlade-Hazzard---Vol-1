import pygame as pg
import random
from settings import *
import tools.collide_checker

class Mob(pg.sprite.Sprite):

    def __init__(self, meteor_images, game):
        pg.sprite.Sprite.__init__(self)
        self.meteor_images = meteor_images
        self.game = game
        self.init()

    def init(self):
        self.image_orig = random.choice(self.meteor_images)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85/ 2)
        self.rect.x = random.randrange(WIDTH-self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pg.time.get_ticks()
        self.life = self.radius


    def rotate(self):
        now = pg.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = pg.time.get_ticks()
            self.rot = (self.rot + self.rot_speed) % 360
            self.image = pg.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.rect = self.image.get_rect()
            self.rect.center = old_center


    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -self.rect.width - 5 or self.rect.right > WIDTH + self.rect.width + 5 :
            if self.game.spawn_enemies:
                self.init()
