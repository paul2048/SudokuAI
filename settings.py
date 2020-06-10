WIDTH = 600
HEIGHT = 600
# PADDING = 20
# MARGIN_TOP = 80

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

test_board = [[0 for x in range(9)] for x in range(9)]

board_pos = {
    "x": 75, #(WIDTH - (HEIGHT - (PADDING + MARGIN_TOP + PADDING))) / 2,
    "y": 100 #MARGIN_TOP + PADDING
}

cell_size = 50
