from ..gamestate import GameState
import pygame as pg
import tools.collide_checker as cc
import gui_overlay.hud as hud
import tools.level_loader as levelloader
import characters.player.player as player
import characters.enemies.mob as mob
import characters.enemies.bosses.boss as boss
from settings import *

class Level2(GameState):
    def __init__(self):
        super(Level2, self).__init__()
        self.score = 0

        self.ll = levelloader.LevelLoader(self, 1)
        self.hud = hud.Hud()

        #Collision checker
        self.collide_checker = cc.CoollideChecker(self)

        # Sprite groups
        self.all_sprites = pg.sprite.Group()
        self.mobs = pg.sprite.Group()
        self.powerups = pg.sprite.Group()
        self.payloads = pg.sprite.Group()
        self.bullets = pg.sprite.Group()
        self.bombs = pg.sprite.Group()

        # Sprites
        for i in range(9):
            self.spawn_mob(self.ll.meteors)
        self.player = player.Player(self)
        # self.boss = Boss(self)
        self.all_sprites.add(self.player)
        # self.all_sprites.add(self.boss)

        # Check for boss fight
        self.spawn_enemies = True
        self.lock_player = False
        self.check_collision_on = True
        self.update_pre_battle = pg.time.get_ticks()
        self.battle_started = False

    def spawn_mob(self, meteors):
        m = mob.Mob(meteors, self)
        self.all_sprites.add(m)
        self.mobs.add(m)

    def startup(self, persistent):
        self.persist = persistent
        self.persist["current_level"] = "LEVEL_2"


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "INGAMEMENU"
            self.done = True

    def update(self, dt):
        self.all_sprites.update()

        # # Start boss battle
        # if self.score >= 100 and not self.battle_started:
        #     self.spawn_enemies = False
        #     self.lock_player = True
        #     self.check_collision_on = False
        #     self.update_pre_battle = pg.time.get_ticks()
        #     print(self.boss.rect.bottom)
        #
        #     if self.boss.rect.bottom < HEIGHT / 4:
        #         self.boss.enter()
        #     else:
        #         self.boss.stop()
        #
        #     if self.boss.rect.bottom >= HEIGHT / 4:
        #         self.boss.dialogue()
        #         self.battle_started = True
        #
        #     # Change to battle music
        #
        # if self.battle_started:
        #     self.lock_player = False
        #     self.check_collision_on = True
        #
        #
        if self.check_collision_on:
            self.collide_checker.player_mobs()
            self.collide_checker.mobs_bullets()
            self.collide_checker.player_powerups()
            if self.battle_started:
                self.collide_checker.boss_bullets()

    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.ll.background, self.ll.background.get_rect())
        self.all_sprites.draw(surface)
        # self.hud.draw(surface)
