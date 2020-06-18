import copy
import random

from settings import *


class Sudoku():
    """
    Sudoku game representation
    """

    def __init__(self):

        self.board = self.new_board()
        self.initial_board = copy.deepcopy(self.board)
        self.selected_cell = None
        self.mouse_pos = None

    def new_board(self):
        """
        """

        return copy.deepcopy(board)

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
                (self.mouse_pos[1] - BOARD_POS[1]) // CELL_SIZE,
                (self.mouse_pos[0] - BOARD_POS[0]) // CELL_SIZE
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
            # If the key is a number, add it to the board
            try:
                int(key)
                self.board[x][y] = int(key)
                # Check for a win
                self.is_win()
            except:
                pass
    
    def is_win(self):
        """
        This method checks if the current state of the board represents
        a win.
        """

        # Iterate through each row of the board
        for i, row in enumerate(self.board):
            # The `i`-th column
            col = [row2[i] for row2 in self.board]

            # Check if the `i`-th row and column are valid
            if not (set(row) == set(col) == set(range(1, 10))):
                return False

        # Mark the victory by "locking" every cell
        self.initial_board = self.board
        return True


class SudokuAI():
    """
    Sudoku game player
    """

    def __init__(self, board):

        self.board = board
        # A dictionary that has pairs of a cell mapping to a set of
        # possible numbers in that cell (e.g: `(1, 4): {1, 2, 9}`)
        self.knowledge = {}
        # When a SudokuAI object is created, initial knowledge
        # will be created
        self.add_initial_knowledge()

    def add_initial_knowledge(self):
        """
        """

        # Iterate through the rows of the board
        for i, row in enumerate(self.board):
            # Iterate through each number of the row
            for j, num in enumerate(row):
                # Add knowledge only to the empty cells
                if self.board[i][j] == 0:
                    cell = (i, j)
                    self.knowledge[cell] = self.possible_nums(cell)

    def reg_nums(self, cell):
        """
        Returns a set of the numbers in the region where `cell` is
        """

        i, j = cell
        # The position of the first cell of the region where `cell` is
        ri, rj = ((i // 3) * 3, (j // 3) * 3)
        region = [
            row[rj:rj+3]
            for row in self.board[ri:ri+3]
        ]

        # Flatten the 2D `region` list
        return set(sum(region, []))

    def row_nums(self, cell):
        """
        Returns a set of the numbers of the row where `cell` is
        """

        i = cell[0]
        row = set(self.board[i])
        row.remove(0)
        return row

    def col_nums(self, cell):
        """
        Returns a set of the numbers of the column where `cell` is
        """

        j = cell[1]
        col = set(row[j] for row in self.board)
        col.remove(0)
        return col

    def possible_nums(self, cell):
        """
        Returns a set of possible numbers that can be inserted in `cell`
        """

        # A set of the numbers that can't be inserted in `cell`
        not_available_nums = self.reg_nums(cell).union(
            self.row_nums(cell).union(
                self.col_nums(cell)
            )
        )

        return set(range(1, 10)).difference(not_available_nums)


    def update_knowledge(self):
        """
        """

        self.add_initial_knowledge()

    def make_move(self):
        """
        """

        # The cells that have only only possible number
        safe_moves = [
            cell for cell in self.knowledge
            if len(self.knowledge[cell]) == 1
        ]

        if safe_moves:
            rand_cell = random.choice(safe_moves)
            i, j = rand_cell
            self.board[i][j] = self.knowledge[rand_cell].pop()
            # print(rand_cell)
            # print(self.board[i][j])
            # print(self.knowledge[rand_cell])
            self.update_knowledge()
            return rand_cell
        else:
            pass
        
