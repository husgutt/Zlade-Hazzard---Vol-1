from .gamestate import GameState
import pygame as pg
from settings import *
from sprites import *
import math
from os import path

class GlobalMapScreen(GameState):
    def __init__(self):
        super(GlobalMapScreen, self).__init__()
        self.title = self.font.render("GlobalMapScreen", True, pg.Color("dodgerblue"))
        self.title_rect = self.title.get_rect(center=self.screen_rect.center)
        self.persist = {}

        self.player_img = pg.image.load(path.join(IMG_FOLDER, PLAYER)).convert()
        self.player_img = pg.transform.scale(self.player_img, (50, 38))
        self.player_img.set_colorkey(BLACK)
        self.player_rect = self.player_img.get_rect()
        self.player_level = 0
        self.player_not_moving = True

        self.level_1 = self.position_level(50,50, GREEN, (WIDTH*1/8,WIDTH*7/8))
        self.level_2 = self.position_level(50,50, RED, (WIDTH*3/8,WIDTH*5/8))
        self.level_3 = self.position_level(50,50, GREEN, (WIDTH*7/8,WIDTH*3/8))

        self.levels_list = []
        self.levels_list =[self.level_1, self.level_2, self.level_3]

        self.lines = []
        self.line_space = 2

    def position_level(self, width, height, color, center):
        level_img = []
        level_image = pg.Surface((width, height))
        level_image.fill(color)
        level_image_rect = level_image.get_rect()
        level_image_rect.center = center
        level_img.append(level_image)
        level_img.append(level_image_rect)
        return level_img


    def startup(self, persistent):
        self.persist = persistent
        self.add_lines_to_plotlist(self.persist)
        if self.persist["animate_on_map"]:
            cleared_level = self.persist["cleared_level"]-1
            if cleared_level < 0:
                self.player_rect.center = (0,0)
            else:
                self.player_rect.center = self.levels_list[cleared_level][1].center
            self.player_level = cleared_level + 1
            self.persist["animate_on_map"] = False

    def get_event(self, event):
        if event.type == pg.QUIT:
            self.quit = True
        keystate = pg.key.get_pressed()
        if keystate[pg.K_ESCAPE]:
            self.next_state = "LEVEL_1"
            self.done = True
        if keystate[pg.K_RIGHT] and self.player_not_moving:
            self.player_level += 1
            if self.player_level > 2:
                self.player_level = 2
        if keystate[pg.K_LEFT] and self.player_not_moving:
            self.player_level -= 1
            if self.player_level < 0:
                self.player_level = 0
        if keystate[pg.K_RETURN] and self.player_not_moving:
            self.next_state = "LEVEL_{}".format(self.player_level + 1)
            self.done = True

    def add_lines_to_plotlist(self, persist):
        step_size = 2

        for i in range (len(self.levels_list)-1):
            x_2 = self.levels_list[i+1][1].center[0]
            y_2 = self.levels_list[i+1][1].center[1]
            x_1 = self.levels_list[i][1].center[0]
            y_1 = self.levels_list[i][1].center[1]

            distance = (x_2 - x_1, y_2 -y_1)
            distance = math.sqrt(distance[0]**2 + distance[1]**2)
            dist_x = x_2 - x_1
            dist_y = y_2 - y_1
            angle = math.atan2(dist_x , dist_y)


            for pos in range(int(distance / 10)):
                pos_x = math.sin(angle)*pos*10 + x_1
                pos_y = math.cos(angle)*pos*10 + y_1
                print(pos_x, pos_y, pos)

                self.lines.append((pos_x, pos_y))

    def move_player(self):
        end_position = self.levels_list[self.player_level][1].center

        x_2 = end_position[0]
        y_2 = end_position[1]
        x_1 = self.player_rect.centerx
        y_1 = self.player_rect.centery

        distance = (x_2 - x_1, y_2 -y_1)
        distance = math.sqrt(distance[0]**2 + distance[1]**2)
        dist_x = x_2 - x_1
        dist_y = y_2 - y_1
        angle = math.atan2(dist_x , dist_y)

        if(self.player_rect.centerx != x_2 and self.player_rect.centery != y_2):
                self.player_not_moving = False
                pos_x = math.sin(angle)*10
                pos_y = math.cos(angle)*10

                self.player_rect.centerx += pos_x
                if(dist_x > 0 and self.player_rect.centerx > x_2):
                    self.player_rect.centerx = x_2
                elif(dist_x < 0 and self.player_rect.centerx < x_2):
                    self.player_rect.centerx = x_2

                self.player_rect.centery += pos_y
                if(dist_y > 0 and self.player_rect.centery > y_2):
                    self.player_rect.centery = y_2
                elif(dist_y < 0 and self.player_rect.centery < y_2):
                    self.player_rect.centery = y_2
        else:
            self.player_not_moving = True

    def update(self, dt):
        self.move_player()



    def draw(self, surface):
        surface.fill(pg.Color("black"))
        for i in range(len(self.lines) - 1):
            if i%self.line_space == 0:
                pg.draw.line(surface, (255, 255, 255), self.lines[i],  self.lines[i+1], 5)
        surface.blit(self.title, self.title_rect)
        surface.blit(self.level_1[0], self.level_1[1])
        surface.blit(self.level_2[0], self.level_2[1])
        surface.blit(self.level_3[0], self.level_3[1])
        surface.blit(self.player_img, self.player_rect)
