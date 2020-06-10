WIDTH = 600
HEIGHT = 600

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHTPURPLE = (130, 130, 178)

test_board = [[0 for x in range(9)] for x in range(9)]

board_pos = (
    75, #(WIDTH - (HEIGHT - (PADDING + MARGIN_TOP + PADDING))) / 2,
    100 #MARGIN_TOP + PADDING
)

board_size = WIDTH - board_pos[0] * 2
cell_size = int(board_size / 9)
