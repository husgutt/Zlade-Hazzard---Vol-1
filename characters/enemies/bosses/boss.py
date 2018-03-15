import pygame as pg
from os import path
from settings import *
from weapons.bullet import *


class Boss(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.boss_img = self.game.ll.boss
        self.image = pg.transform.scale(self.boss_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH / 2
        self.rect.bottom = 5
        self.speedx = 0
        self.speedy = 0
        self.shield = 100
        self.shoot_delay = 200
        self.last_shot = pg.time.get_ticks()
        self.lives = 0
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()
        self.entering = False

        #sounds
        self.shoot_sound = pg.mixer.Sound(path.join(SND_FOLDER, 'Laser_Shoot2.wav'))

    def update(self):

        self.speedy = 0
        # Entering:
        if self.entering:
            self.speedy = 2

        self.rect.y += self.speedy

        # timeput for powerups
        if self.power >= 2 and pg.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pg.time.get_ticks()
        # unhide if hidden
        if self.hidden and pg.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.x = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
        self.speedx = 0


    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                self.shoot_sound.play()
                bullet = Bullet(self.rect.centerx, self.rect.top, 90, self.game)
                self.game.all_sprites.add(bullet)
                self.game.bullets.add(bullet)

    def enter(self):
        self.entering = True
    def stop(self):
        self.entering = False

    def dialogue(self):
        pass


    def hide(self):
        # hide the boss
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
