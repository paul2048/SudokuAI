from settings import *

class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        self.board = test_board
        self.selected_cell = None
        self.mouse_pos = None

    def get_cell(self, board_rect):
        """
        If the mouse was clicked outside the board, the method returns
        `False`, else it returns the position of the clicked cell (e.g:
        `(8, 8)` will be returned for clicking the last cell). `board_rect`
        is a pygame `Rect` with the size and position of the board.
        """

        # If the clicked coordonates are inside the board
        if board_rect.collidepoint(self.mouse_pos):
            # Return the position of the clicked cell
            return (
                (self.mouse_pos[0] - BOARD_POS[0]) // CELL_SIZE,
                (self.mouse_pos[1] - BOARD_POS[1]) // CELL_SIZE
            )

        return False
