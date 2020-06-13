WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (239, 52, 52)
GREEN = (26, 255, 26)
LIGHTPURPLE = (130, 130, 178)
LIGHTGRAY = (210, 210, 210)

# Board position and size
BOARD_POS = (75, 100)
BOARD_SIZE = WIDTH - BOARD_POS[0] * 2
CELL_SIZE = int(BOARD_SIZE / 9)

# The path of the song in the instructions menu
SONG_PATH = None  # "assets/sounds/instructions.mp3"

# The color of UI parts
SELECTED_CELL_COLOR = LIGHTPURPLE
INITIAL_CELL_COLOR = LIGHTGRAY

board = [
    [0,3,0,0,0,2,8,0,0],
    [0,0,9,0,0,4,0,0,0],
    [0,0,7,6,1,0,4,0,3],
    [0,5,0,1,0,6,0,3,4],
    [0,8,1,0,2,0,6,7,0],
    [6,9,0,5,0,7,0,8,0],
    [3,0,8,0,6,1,5,0,0],
    [0,0,0,4,0,0,7,0,0],
    [0,0,5,7,0,0,0,1,0],
]
