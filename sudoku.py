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
        self.mouse_pos = (0, 0)

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
        i, j = self.get_cell(board_rect)

        # Check if the `(i, j)` is a valid board position
        if self.initial_board[i][j] == 0:
            # If the key is a number, add it to the board
            try:
                int(key)
                self.board[i][j] = int(key)
                # Check for a win
                self.is_win()
            except:
                pass
    
    def is_win(self):
        """
        This method checks if the current state of the board represents
        a win. If it's a win, "lock" the board
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
        self.update_knowledge()

    def update_knowledge(self, board=[], knowledge=[]):
        """
        Updates the knowledge of 1 or more cells by reducing the number of
        valid numbers that can be inserted in the specfic cell.
        The optional arguments `board` and `knowledge` are used when the
        live board and knowledge musn't be updated (used while backtracking). 
        """

        board = board if board else self.board
        knowledge = knowledge if knowledge else self.knowledge

        # Iterate through the rows of the board
        for i, row in enumerate(board):
            # Iterate through each number of the row
            for j, num in enumerate(row):
                # Add knowledge only to the empty cells
                if board[i][j] == 0:
                    cell = (i, j)
                    knowledge[cell] = self.possible_nums(cell, board)

    def possible_nums(self, cell, board):
        """
        Returns a set of possible numbers that can be inserted in `cell`
        """

        i, j = cell
        # A set of the numbers in the row where `cell` is
        row = set(board[i])
        # A set of the numbers in the column where `cell` is
        col = set(row[j] for row in board)
        # The position of the first cell of the region where `cell` is
        ri, rj = ((i // 3) * 3, (j // 3) * 3)
        # A set of the numbers in the region where `cell` is
        reg = set(
            num for row in board[ri:ri+3]
            for num in row[rj:rj+3]
        )

        # A set of the numbers that can't be inserted in `cell`
        not_available_nums = row.union(col.union(reg))
        not_available_nums.remove(0)

        return set(range(1, 10)).difference(not_available_nums)

    def is_win(self, board):
        """
        This method checks if the current state of the board represents
        a win.
        """

        # Iterate through each row of the board
        for i, row in enumerate(board):
            # The `i`-th column
            col = [row2[i] for row2 in board]

            # Check if the `i`-th row and column are valid
            if not (set(row) == set(col) == set(range(1, 10))):
                return False

        return True

    def is_board_valid(self, board, knowledge):
        """
        """

        # Iterate through each row of the board
        for i, row in enumerate(board):
            # If an empty cell has no knowledge associated with the cell
            for j, num in enumerate(row):
                cell = (i, j)
                if num == 0 and len(knowledge[cell]) == 0:
                    return False

            # The numbers of the i-th row (without 0s)
            row = [num for num in row if num]
            # The numbers of the i-th column (without 0s)
            col = [row2[i] for row2 in board if row2[i]]
            # The numbers of the i-th region (without 0s)
            ri, rj = (i * 3, (i // 3) * 3)
            reg = [
                num for row2 in self.board[ri:ri+3]
                for num in row2[rj:rj+3] if num
            ]

            # If a number was repeated in a row, column or region
            if len(row) != len(set(row)) or \
               len(col) != len(set(col)) or \
               len(reg) != len(set(reg)):
                return False

        return True

    def make_move(self):
        """
        """

        # The cells that have only 1 possible number
        safe_moves = [
            cell for cell in self.knowledge
            if len(self.knowledge[cell]) == 1
        ]

        # If 1 or more safe moves are available
        if safe_moves:
            print("Normal move, bro........")
            # Make a random safe move
            safe_cell = i, j = random.choice(safe_moves)
            self.board[i][j] = self.knowledge[safe_cell].pop()
            self.update_knowledge()
            return safe_cell
        # If no safe moves are available
        else:
            print("RISKY MOVE!!!!!!!!!!!!!")
            # Get the cells with the smallest amount of possible numbers
            # that a cell on the current board can have
            min_num = min(
                len(nums) for nums in self.knowledge.values()
                if len(nums)
            )
            best_moves = [
                cell for cell in self.knowledge
                if len(self.knowledge[cell]) == min_num
            ]

            board_cpy = copy.deepcopy(self.board)
            knowledge_cpy = copy.deepcopy(self.knowledge)
            safe_cell, safe_num = self.backtrack(board_cpy, knowledge_cpy)
            i, j = safe_cell
            self.board[i][j] = safe_num
            self.knowledge[safe_cell] = set()
            self.update_knowledge()
            return safe_cell

    def backtrack(self, board, knowledge, guess=(None, None)):
        """
        """

        if self.is_win(board):
            return guess

        safe_moves = [
            cell for cell in knowledge
            if len(knowledge[cell]) == 1
        ]

        while safe_moves:
            if self.is_board_valid(board, knowledge):
                safe_cell = i, j = random.choice(safe_moves)
                board[i][j] = knowledge[safe_cell].pop()
                self.update_knowledge(board, knowledge)
                safe_moves = [
                    cell for cell in knowledge
                    if len(knowledge[cell]) == 1
                ]
                print(safe_cell)
            else:
                return False

        if self.is_win(board):
            return guess

        if not safe_moves:
            if self.is_board_valid(board, knowledge):
                min_num = min(
                    len(nums) for nums in knowledge.values()
                    if len(nums)
                )
                best_moves = [
                    cell for cell in knowledge
                    if len(knowledge[cell]) == min_num
                ]

                rand_cell = i, j = random.choice(best_moves)

                for num in knowledge[rand_cell]:
                    new_board = copy.deepcopy(board)
                    new_knowledge = copy.deepcopy(knowledge)
                    new_board[i][j] = num
                    new_knowledge[rand_cell] = set()
                    self.update_knowledge(new_board, new_knowledge)
                    result = self.backtrack(new_board, new_knowledge, (rand_cell, num))
                    if self.is_win(board):
                        return (rand_cell, num)
                    elif type(result) == tuple:
                        return result
            else:
                return False

        if self.is_win(board):
            return guess
