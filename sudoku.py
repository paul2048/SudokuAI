import copy

from settings import *


class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        self.board = board
        self.initial_board = copy.deepcopy(board)
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

    def insert_num(self, window, board_rect, key):
        """
        This method checks if the pressed key is a number, and if so,
        the number will be inserted in the selected cell.
        """

        # Get the click cell position (e.g: `(8, 8)` is the last cell)
        x, y = self.get_cell(board_rect)

        # Check if the `(x, y)` is a valid board position
        if self.initial_board[x][y] == 0:
            try:
                int(key)
                self.board[x][y] = key
            except:
                pass
