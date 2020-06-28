WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (239, 52, 52)
GREEN = (26, 255, 26)
LIGHT_GRAY = (200, 200, 200)
DARK_GRAY = (24, 24, 24)
ANTIQUE_WHITE = (238, 212, 210)
DARK_SLATE_GRAY = (40, 75, 75)

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
SONG_PATH = "assets/sounds/menu.mp3"
SONG = SONG_PATH

# Play with a predefined board if you want. If a number
# from 1 to 9 is added below, `BOARD` will be used.
BOARD = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
]
