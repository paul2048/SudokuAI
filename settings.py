WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (239, 52, 52)
GREEN = (26, 255, 26)
LIGHTPURPLE = (130, 130, 178)

# Board position and size
BOARD_POS = (75, 100)
BOARD_SIZE = WIDTH - BOARD_POS[0] * 2
CELL_SIZE = int(BOARD_SIZE / 9)

# The path of the song in the instructions menu
SONG_PATH = None  # "assets/sounds/instructions.mp3"

# The color of the selected cell
selected_cell_color = LIGHTPURPLE

test_board = [[0 for x in range(9)] for x in range(9)]
