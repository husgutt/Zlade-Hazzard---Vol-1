import pygame as pg
from os import path
from settings import *
from weapons.bullet import *

class Player(pg.sprite.Sprite):
    def __init__(self, game):
        pg.sprite.Sprite.__init__(self)
        self.game = game
        self.player_img = self.game.ll.player
        self.image = pg.transform.scale(self.player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        # pg.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 200
        self.last_shot = pg.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pg.time.get_ticks()
        self.power = 1
        self.power_time = pg.time.get_ticks()

        #sounds
        self.shoot_sound = pg.mixer.Sound(path.join(SND_FOLDER, 'Laser_Shoot2.wav'))

    def update(self):
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
        keystate = pg.key.get_pressed()
        if keystate[pg.K_LEFT]:
            self.speedx = -8
        if keystate[pg.K_RIGHT]:
            self.speedx = 8
        if keystate[pg.K_SPACE] and not self.game.lock_player:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.x < 0:
            self.rect.x = 0

    def powerup(self):
        self.power += 1
        if self.power > MAX_POWERUP_LEVEL:
            self.power = MAX_POWERUP_LEVEL
        self.power_time = pg.time.get_ticks()

    def shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                self.shoot_sound.play()
                bullet = Bullet(self.rect.centerx, self.rect.top, 90, self.game)
                self.game.all_sprites.add(bullet)
                self.game.bullets.add(bullet)
            if self.power == 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery, 90)
                bullet2 = Bullet(self.rect.right, self.rect.centery, 90)
                self.shoot_sound.play()
                self.game.all_sprites.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
                self.shoot_delay = 200
            if self.power == 3:
                bullet1 = Bullet(self.rect.left, self.rect.centery, 90)
                bullet2 = Bullet(self.rect.right, self.rect.centery, 90)
                self.shoot_sound.play()
                self.game.all_sprites.add(bullet1)
                self.game.all_sprites.add(bullet2)
                self.game.bullets.add(bullet1)
                self.game.bullets.add(bullet2)
                self.shoot_delay = 100
            if self.power == 4:
                self.shoot_sound.play()
                for i in range(BULLET_DIRECTIONS + 1):
                    bullet = Bullet(self.rect.centerx, self.rect.top, (90 / BULLET_DIRECTIONS)*i + 45)
                    self.game.all_sprites.add(bullet)
                    self.game.bullets.add(bullet)
                    self.shoot_delay = 200
            if self.power >= MAX_POWERUP_LEVEL:
                self.shoot_sound.play()
                payload = Payload(self.rect.centerx, self.rect.top)
                self.game.all_sprites.add(payload)
                self.game.payloads.add(payload)
                self.shoot_delay = 1000



    def hide(self):
        # hide the player
        self.hidden = True
        self.hide_timer = pg.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)
