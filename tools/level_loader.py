import pygame as pg
from sprites import *
from settings import *
from os import path
from characters.player.player import Player

# Load images and sounds

class LevelLoader():
    def __init__(self, game, level):

        self.current_level = level
        self.score = 0
        self.game = game
        self.player = self.load_player()
        self.player_lives = self.load_player_life()
        self.meteors = self.load_meteors()
        self.boss = self.load_boss()
        self.background = self.load_background()
        self.pow = self.load_pow()
        self.weapons = self.load_weapons()
        self.explosion = self.load_explosions()
        self.snd_fx = self.load_snd_fx()
        self.music = self.load_music()

    def load_player(self):
        return  pg.image.load(path.join(IMG_FOLDER, PLAYER)).convert()

    def load_player_life(self):
        return  pg.transform.scale(self.player, (25, 19))

    def load_meteors(self):
            meteors = []
            for img in METEORS[str(self.current_level)]:
                meteors.append(pg.image.load(path.join(IMG_FOLDER, img,)).convert())
            return meteors

    def load_boss(self):
        return  pg.image.load(path.join(IMG_FOLDER, PLAYER)).convert()

    def load_background(self):
        return pg.image.load(path.join(IMG_FOLDER, BACKGROUND[self.current_level-1])).convert()

    def load_weapons(self):
        weapons = []
        for img in WEAPONS[str(self.current_level)]:
            weapons.append(pg.image.load(path.join(IMG_FOLDER, img,)).convert())
        return weapons

    def load_explosions(self):
        explosion_anim = {}
        explosion_anim['lg'] = []
        explosion_anim['sm'] = []
        explosion_anim['player'] = []
        for i in range(9):
            filename = 'regularExplosion0{}.png'.format(i)
            img = pg.image.load(path.join(IMG_FOLDER, filename)).convert()
            img.set_colorkey(BLACK)
            img_lg = pg.transform.scale(img, (75, 75))
            explosion_anim['lg'].append(img_lg)
            img_sm = pg.transform.scale(img, (32, 32))
            explosion_anim['sm'].append(img_sm)
            filename = 'sonicExplosion0{}.png'.format(i)
            img = pg.image.load(path.join(IMG_FOLDER, filename)).convert()
            img.set_colorkey(BLACK)
            explosion_anim['player'].append(img)
        return explosion_anim

    def load_pow(self):
        powerup_images = {}
        powerup_images['shield'] = pg.image.load(path.join(IMG_FOLDER, 'powerupBlue_shield.png'))
        powerup_images['gun'] = pg.image.load(path.join(IMG_FOLDER, 'bolt_gold.png'))
        return powerup_images

    def load_snd_fx(self):
        pass

    def load_music(self):
        pass
