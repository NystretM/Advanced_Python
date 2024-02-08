import os
# Konstanten zur dynamischen Optimierung des Spiels

# GENERELL
WINDOW_NAME = "Runner"
PATH = os.path.dirname(os.path.abspath(__file__)) + "/"
FPS = 60
SCREEN_SIZE_X = 1200
SCREEN_SIZE_Y = 800
START_GAME_SPEED = 0
MAX_GAME_SPEED = 3
ENDSCREEN_TIME = 5

# FARBEN
BG_COLOR = (254, 250, 224)
GROUND_COLOR = (204, 213, 174)
PLAYER_COLOR = (212, 163, 115)
STAGE_COLOR = (233, 237, 201)
OBSTACLE_COLOR = (235, 102, 73)
COIN_COLOR = (235, 227, 73)
FONT_COLOR = (0, 3, 0)

# SPIELER
PLAYER_OFFSET_X = 50
PLAYER_SIZE = 69
PLAYER_SPEED = 7
JUMP_FORCE = 30
GRAVITY = 2

# HINDERNISSE
OBSTACLE_SIZE_TO_PLAYER_RATIO = 1.5
OBSTACLE_SPEED = 5
OBSTACLE_MAX = 4
OBSTACLE_INTERVAL_TIME = 4

# PUNKTE
SCORE_TIME_MUL = 10
SCORE_COIN = 90
SCORE_FONT = None
SCORE_FONT_SIZE = 50
SCORE_PATH = PATH + 'score.txt'

# Sounds für Sprung und Coin sammeln
JUMP_PATH = PATH + 'jump.mp3'
COIN_PATH = PATH + 'coin.mp3'