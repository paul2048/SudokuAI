WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (239, 52, 52)
GREEN = (26, 255, 26)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (24, 24, 24)
ANTIQUE_WHITE = (240, 230, 210)
DARK_SLATE_GRAY = (47, 79, 79)

# Board position and size
BOARD_POS = (75, 100)
BOARD_SIZE = WIDTH - BOARD_POS[0] * 2
CELL_SIZE = int(BOARD_SIZE / 9)

# Turn dark mode on or off
DARK_MODE = True

# The color of UI parts based on theme
if DARK_MODE:
    THEME_COLOR_1 = BLACK
    THEME_COLOR_2 = WHITE
    SELECTED_CELL_COLOR = DARK_GRAY
    INITIAL_CELL_COLOR = DARK_SLATE_GRAY
else:
    THEME_COLOR_1 = WHITE
    THEME_COLOR_2 = BLACK
    SELECTED_CELL_COLOR = ANTIQUE_WHITE
    INITIAL_CELL_COLOR = LIGHT_GRAY

# The path of the song in the instructions menu
SONG_PATH = "assets/sounds/instructions.mp3"
SONG = SONG_PATH

board = [
    [0,3,4,0,0,2,8,0,0],
    [0,0,9,0,0,4,0,0,0],
    [0,0,7,0,1,0,4,0,3],
    [0,0,2,1,8,6,9,3,4],
    [0,0,1,0,2,0,6,7,5],
    [6,0,3,5,0,7,0,8,0],
    [3,0,8,0,6,1,5,0,0],
    [0,0,6,4,0,0,7,0,0],
    [0,0,5,7,0,0,0,1,0],
]
