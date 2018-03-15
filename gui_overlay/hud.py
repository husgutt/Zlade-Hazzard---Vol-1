from tools.tools import Tools
from settings import *

class Hud():
    def __init__(self):
        self.tools = Tools()

    def draw(self, surface, player, ll, level, score):
        self.tools.draw_text(surface, str(score), 18, WIDTH/2, 10)
        # self.tools.draw_text(surface, str(level), 22, WIDTH/2, 20)
        self.tools.draw_shield_bar(surface, 5, 5, player.shield)
        self.tools.draw_lives(surface, WIDTH-100, 5, player.lives, ll.player_lives)
