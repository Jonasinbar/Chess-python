UP_DIRECTION = "UP"
DOWN_DIRECTION = "DOWN"
SIZE_BOARD = 8
PLAYER_1_DIRECTION = UP_DIRECTION
PLAYER_2_DIRECTION = DOWN_DIRECTION
PLAYER_1_COLOR = "black"
PLAYER_2_COLOR = "white"
WIDTH = 1500
HEIGHT = 800
MARGIN = 60
BOARD_LINE_WIDTH = 3
WHITE = (255, 255, 255)
GREY = (112, 112, 112)
BLACK = (0, 0, 0)
BROWN = (150, 75, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BOARD_COLOR = BLACK
UP_LEFT = (MARGIN, MARGIN)
DOWN_RIGHT = (min(WIDTH, HEIGHT) - MARGIN, min(WIDTH, HEIGHT) - MARGIN)
if SIZE_BOARD:
    SQUARE_SIZE = (DOWN_RIGHT[0] - UP_LEFT[0]) / SIZE_BOARD
PLAYER_1_COLOR_SELECTED = (153, 204, 255)
PLAYER_2_COLOR_SELECTED = (255, 153, 253)
IMGS_DIR = 'assets/images/'