import pygame as pg

class Bomb(pg.sprite.Sprite):

    def __init__(self, center):
        pg.sprite.Sprite.__init__(self)
        self.radius = 300
        self.image = pg.Surface((self.radius, self.radius))
        self.rect = self.image.get_rect()
        self.rect.center = center
        pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.image.set_colorkey(BLACK)
        self.last_update = pg.time.get_ticks()
        self.delay = 10

    def update(self):
        if pg.time.get_ticks() - self.last_update > self.delay:
            print("bomb")
            self.kill()
