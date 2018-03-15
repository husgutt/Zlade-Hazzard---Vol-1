import sys

import pygame as pg
from settings import *
from states.menu.startscreen import SplashScreen
from states.menu.in_game import InGameMenuScreen
from states.menu.start_new_game import NewGame
from states.menu.load_game import LoadGame
from states.cutscenes.intro_level_1 import IntroLevel1
from states.cutscenes.outro_level_1 import OutroLevel1
from states.global_map import GlobalMapScreen
from states.scorescreen import ScoreScreen
from states.levels.level_1 import Level1
from states.levels.level_2 import Level2


class Game(object):

    def __init__(self, screen, states, start_state):
        self.done = False
        self.screen = screen
        self.clock = pg.time.Clock()
        self.fps = 60
        self.states = states
        self.state_name = start_state
        self.state = self.states[self.state_name]

    def event_loop(self):
        """Events are passed for handling to the current state."""
        for event in pg.event.get():
            self.state.get_event(event)

    def flip_state(self):
        """Switch to the next game state."""
        current_state = self.state_name
        next_state = self.state.next_state
        self.state.done = False
        self.state_name = next_state
        persistent = self.state.persist
        self.state = self.states[self.state_name]
        self.state.startup(persistent)

    def update(self, dt):
        """
        Check for state flip and update active state.

        dt: milliseconds since last frame
        """
        if self.state.quit:
            self.done = True
        elif self.state.done:
            self.flip_state()
        self.state.update(dt)

    def draw(self):
        """Pass display surface to active state for drawing."""
        self.state.draw(self.screen)

    def run(self):
        """
        Pretty much the entirety of the game's runtime will be
        spent inside this while loop.
        """
        while not self.done:
            dt = self.clock.tick(self.fps)
            self.event_loop()
            self.update(dt)
            self.draw()
            pg.display.update()


if __name__ == "__main__":
    pg.mixer.pre_init(44100, -16, 1, 512)
    pg.init()
    pg.mixer.init()
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    pg.display.set_caption(TITLE)
    states = {"SPLASH": SplashScreen(),
              "LEVEL_1": Level1(),
              "LEVEL_2": Level2(),
              "INTRO_LEVEL_1": IntroLevel1(),
              "GLOBAL_MAP": GlobalMapScreen(),
              "SCORE": ScoreScreen(),
              "OUTRO_LEVEL_1": OutroLevel1(),
              "INGAMEMENU": InGameMenuScreen(),
              "NEWGAME": NewGame(),
              "LOADGAME": LoadGame(),}
    game = Game(screen, states, "SPLASH")
    game.run()
    pg.quit()
    sys.exit()
