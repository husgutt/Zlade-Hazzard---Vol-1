from os import path

TITLE = "Shmup"
WIDTH = 480
HEIGHT = 600
FPS = 60

# Colors
BLACK = (0,0,0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

POWERUP_TIME = 5000
MAX_POWERUP_LEVEL = 5
BULLET_DIRECTIONS = 10
LEVEL_STEP = 10000
MAX_LEVEL = 60

# Dir
GAME_FOLDER = path.dirname(__file__)
IMG_FOLDER = path.join(GAME_FOLDER, "img")
SND_FOLDER = path.join(GAME_FOLDER, "snd")
