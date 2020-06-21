WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (239, 52, 52)
GREEN = (26, 255, 26)
ANTIQUE_WHITE = (240, 230, 210)
LIGHTGRAY = (200, 200, 200)

# Board position and size
BOARD_POS = (75, 100)
BOARD_SIZE = WIDTH - BOARD_POS[0] * 2
CELL_SIZE = int(BOARD_SIZE / 9)

# The path of the song in the instructions menu
SONG_PATH = None  # "assets/sounds/instructions.mp3"

# The color of UI parts
SELECTED_CELL_COLOR = ANTIQUE_WHITE
INITIAL_CELL_COLOR = LIGHTGRAY

# board = [
#     [0,3,0,0,0,2,8,0,0],
#     [0,0,9,0,0,4,0,0,0],
#     [0,0,7,6,1,0,4,0,3],
#     [0,5,0,1,0,6,0,3,4],
#     [0,8,1,0,2,0,6,7,0],
#     [6,9,0,5,0,7,0,8,0],
#     [3,0,8,0,6,1,5,0,0],
#     [0,0,0,4,0,0,7,0,0],
#     [0,0,5,7,0,0,0,1,0],
# ]

board = [
    [0,3,0,0,0,2,8,0,0],
    [0,0,9,0,0,4,0,0,0],
    [0,0,7,0,1,0,4,0,3],
    [0,5,0,1,0,6,0,3,4],
    [0,0,1,0,2,0,6,7,0],
    [6,0,0,5,0,7,0,8,0],
    [3,0,8,0,6,1,5,0,0],
    [0,0,0,4,0,0,7,0,0],
    [0,0,5,7,0,0,0,1,0],
]
# board = [
#     [6, 0, 4, 1, 9, 7, 2, 3, 8],
#     [9, 2, 7, 8, 3, 5, 4, 1, 6],
#     [1, 3, 8, 2, 4, 6, 5, 9, 7],
#     [3, 8, 1, 7, 6, 4, 9, 5, 2],
#     [4, 9, 2, 5, 8, 3, 7, 6, 1],
#     [7, 6, 5, 9, 1, 2, 8, 4, 3],
#     [8, 4, 6, 3, 7, 0, 1, 2, 5],
#     [5, 7, 3, 4, 2, 1, 6, 8, 9],
#     [2, 1, 9, 6, 5, 8, 3, 7, 4],
# ]
