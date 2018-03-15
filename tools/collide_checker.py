import pygame as pg
from weapons.bomb import *
import random
from settings import *

class CoollideChecker():
    def __init__(self, game):
        self.game = game

    def player_powerups(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.powerups, True)
        for hit in hits:
            if hit.type == 'shield':
                self.game.player.shield += random.randrange(10, 30)
                if self.game.player.shield >= 100:
                    self.game.player.shield = 100
            if hit.type == 'gun':
                self.game.player.powerup()

    def mobs_payloads(self):
        hits = pg.sprite.groupcollide(self.game.mobs, self.game.payloads, False, True)
        for hit in hits:
            random.choice(expl_sounds).play()
            bomb = Bomb(hit.rect.center)
            self.game.all_sprites.add(bomb)
            self.game.bombs.add(bomb)

    def mobs_bombs(self):
        hits = pg.sprite.groupcollide(self.game.mobs, self.game.bombs, False, False, pg.sprite.collide_circle)
        for hit in hits:
            hit.life -= 60
            if hit.life <= 0:
                if random.random() > 0.9:
                    pow = Pow(hit.rect.center)
                    self.game.all_sprites.add(pow)
                    self.game.powerups.add(pow)
                self.game.score += 60 - hit.radius
                expl = Explosion(hit.rect.center, 'lg')
                self.game.all_sprites.add(expl)
                hit.kill()
                if self.game.spawn_enemies:
                    self.game.spawn_mob(self.game.ll.meteor)

    def mobs_bullets(self):
        hits = pg.sprite.groupcollide(self.game.mobs, self.game.bullets, False, True)
        for hit in hits:
            hit.life -= 10
            if hit.life <= 0:
                # if random.random() > 0.7:
                #     pow = Pow(hit.rect.center)
                #     self.game.all_sprites.add(pow)
                #     self.game.powerups.add(pow)
                # random.choice(expl_sounds).play()
                self.game.score += 60 - hit.radius
                # expl = Explosion(hit.rect.center, 'lg')
                # self.game.all_sprites.add(expl)
                hit.kill()
                if self.game.spawn_enemies:
                    self.game.spawn_mob(self.game.ll.meteors)
            else:
                pass
                # expl = Explosion(hit.rect.center, 'sm')
                # self.game.all_sprites.add(expl)

    def boss_bullets(self):
        hits = pg.sprite.spritecollide(self.game.boss, self.game.bullets, True, pg.sprite.collide_circle)
        for hit in hits:
            # boss_hit.play()

            # expl = Explosion(hit.rect.center, 'sm')
            # self.game.all_sprites.add(expl)
            self.game.boss.shield -= 30
            if self.game.boss.shield <= 0:
                # player_die_sound.play()
                self.game.level_win = True
                self.game.playing = False
                self.game.boss.kill()
                # death_explosion = Explosion(player.rect.center, 'player')
                # self.game.all_sprites.add(death_explosion)

    def player_mobs(self):
        hits = pg.sprite.spritecollide(self.game.player, self.game.mobs, True, pg.sprite.collide_circle)
        for hit in hits:
            # player_hit.play()
            if self.game.spawn_enemies:
                self.game.spawn_mob(self.game.ll.meteors)
            # expl = Explosion(hit.rect.center, 'sm')
            # self.game.all_sprites.add(expl)
            self.game.player.shield -= hit.radius * 2
            if self.game.player.shield <= 0 and self.game.player.alive():
                # player_die_sound.play()
                self.game.player.hide()
                self.game.player.lives -= 1
                self.game.player.shield = 100
                if self.game.player.lives <= 0:
                    self.game.game_over = True
                    self.game.playing = False
                # death_explosion = Explosion(player.rect.center, 'player')
                # self.game.all_sprites.add(death_explosion)
