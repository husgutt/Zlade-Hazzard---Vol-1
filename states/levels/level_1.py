from ..gamestate import GameState
import pygame as pg
import tools.collide_checker as cc
import gui_overlay.hud as hud
import tools.level_loader as levelloader
import characters.player.player as player
import characters.enemies.mob as mob
import characters.enemies.bosses.boss as boss
from settings import *
import tools.textrectexception as tre

class Level1(GameState):
    def __init__(self):
        super(Level1, self).__init__()
        self.score = 0
        self.level = 1

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
        self.boss = boss.Boss(self)
        self.all_sprites.add(self.player)
        self.all_sprites.add(self.boss)

        # Check for boss fight
        self.spawn_enemies = True
        self.lock_player = False
        self.check_collision_on = True
        self.update_pre_battle = pg.time.get_ticks()
        self.battle_started = False

        # Dialogue
        self.in_dialogue = False
        self.output = ""
        self.count = 0
        self.delay = 0
        self.message_number = 0
        self.message = ["Hei din fjomp, vil du gå videre? Trykk enter da...",
                        "Veldig bra jobba! Imponerende. \nDu er god til å trykke på knapper",
                        "Det kommer godt med.",
                        "Trykk... trykk.... trykk...",
                        "ÅÅåå så flink!",
                        "Er mamma stolt?"]
        self.blink_active = False
        self.blink_delay = 0
        self.blink = None

    def boss_dialogue(self):
        self.in_dialogue = True
        font = pg.font.Font(None, 22)
        height = 100
        rect = pg.Rect((0,HEIGHT - height,WIDTH,height))
        text_color = WHITE
        background_color = BLACK
        return_list = [tre.render_textrect(self.output, font, rect, text_color, background_color, justification=0)]
        return_list.append(rect)
        return return_list

    def update_text(self, dt):
        self.delay += dt
        if self.count <= len(self.message[self.message_number]) and self.delay > 50 :
            self.output = self.message[self.message_number][0:self.count]
            self.count += 1
            self.delay = 0
        self.blink_delay += dt
        if self.blink_delay > 300:
            self.blink_active = not self.blink_active
            self.blink_delay = 0



    def spawn_mob(self, meteors):
        m = mob.Mob(meteors, self)
        self.all_sprites.add(m)
        self.mobs.add(m)

    def startup(self, persistent):
        self.persist = persistent
        self.persist["current_level"] = "LEVEL_1"


    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "INGAMEMENU"
            self.done = True
        if keystate[pg.K_RETURN]:
            if self.in_dialogue:
                if self.count >= len(self.message[self.message_number]):
                    self.count = 0
                    self.message_number += 1
                else:
                     self.count = len(self.message[self.message_number])-1
                if self.message_number == len(self.message):
                    self.battle_started = True
                    self.in_dialogue = False
                    self.message_number = 0


    def update(self, dt):
        self.all_sprites.update()

        # Start boss battle
        if self.score >= 100 and not self.battle_started:
            self.spawn_enemies = False
            self.lock_player = True
            self.check_collision_on = False
            self.update_pre_battle = pg.time.get_ticks()
            print(self.boss.rect.bottom)

            if self.boss.rect.bottom < HEIGHT / 4:
                self.boss.enter()
            else:
                self.boss.stop()

            if self.boss.rect.bottom >= HEIGHT / 4:
                self.boss_dialogue()

            # Change to battle music
        if self.in_dialogue:
            self.update_text(dt)

        if self.battle_started:
            self.lock_player = False
            self.check_collision_on = True


        if self.check_collision_on:
            self.collide_checker.player_mobs()
            self.collide_checker.mobs_bullets()
            self.collide_checker.player_powerups()
            if self.battle_started:
                self.collide_checker.boss_bullets()

        if self.boss.shield <= 0:
            self.persist["level_1_score"] = self.score
            self.persist["cleared_level"] = 1
            self.persist["cleared_level_score"] = self.score
            self.persist["level_1_cleared"] = True
            self.persist["animate_on_map"] = True
            self.next_state = "SCORE"
            self.done = True



    def draw(self, surface):
        surface.fill(BLACK)
        surface.blit(self.ll.background, self.ll.background.get_rect())
        self.all_sprites.draw(surface)
        self.hud.draw(surface, self.player, self.ll,  self.level, self.score)
        if self.in_dialogue:
            text = self.boss_dialogue()
            surface.blit(text[0], text[1])
